from __future__ import annotations

import math
import re
from typing import Any


_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def _norm(value: Any) -> str:
    return str(value).casefold().strip() if value is not None else ""


def _num(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = _norm(value).replace(",", "")
    match = _NUM_RE.search(text)
    return float(match.group()) if match else None


def get_field(record: dict, field: str) -> Any:
    key = field.casefold()

    aliases = {
        "product_category": ("product_category",),
        "sku_id": ("product_sku",),
        "product_sku": ("product_sku",),
        "factory_name": ("factory_offer", "factory_name"),
        "material": ("factory_offer", "material"),
        "material_detail": ("factory_offer", "material_detail"),
        "price": ("factory_offer", "price"),
        "moq": ("factory_offer", "moq"),
        "size_system": ("factory_offer", "size_system"),
        "size_range": ("factory_offer", "size_range"),
        "function_tags": ("product", "function_tags"),
        "scenario_tags": ("product", "scenario_tags"),
        "special_features": ("product", "special_features"),
    }
    path = aliases.get(key)
    if path is not None:
        cur: Any = record
        for part in path:
            cur = cur.get(part) if isinstance(cur, dict) else None
        return cur

    perf = record.get("product", {}).get("performance_attributes", {}) or {}
    for k, value in perf.items():
        if str(k).casefold() == key:
            return value

    return None


def _contains(actual: Any, expected: Any) -> bool:
    if isinstance(actual, list):
        e = _norm(expected)
        return any(e == _norm(item) or e in _norm(item) for item in actual)
    return _norm(expected) in _norm(actual)


def condition_match(record: dict, condition: dict) -> bool:
    field = str(condition.get("field", ""))
    op = str(condition.get("op", "eq")).casefold()
    expected = condition.get("value")
    actual = get_field(record, field)

    if op == "contains":
        return _contains(actual, expected)

    if op == "eq":
        an, en = _num(actual), _num(expected)
        if an is not None and en is not None:
            return math.isclose(an, en, rel_tol=1e-9, abs_tol=1e-9)
        return _norm(actual) == _norm(expected)

    if op == "neq":
        return not condition_match(record, {**condition, "op": "eq"})

    if op in {"lte", "gte", "lt", "gt"}:
        an, en = _num(actual), _num(expected)
        if an is None or en is None:
            return False
        return {
            "lte": an <= en,
            "gte": an >= en,
            "lt": an < en,
            "gt": an > en,
        }[op]

    if op == "range":
        if not isinstance(expected, list) or len(expected) != 2:
            return False
        an = _num(actual)
        low, high = _num(expected[0]), _num(expected[1])
        return an is not None and low is not None and high is not None and low <= an <= high

    if op == "in":
        if not isinstance(expected, list):
            return False
        return any(
            condition_match(record, {"field": field, "op": "eq", "value": x})
            for x in expected
        )

    raise ValueError(f"不支持的条件操作符：{op}")


def soft_match_value(record: dict, condition: dict) -> float:
    if condition_match(record, condition):
        return 1.0

    field = str(condition.get("field", ""))
    op = str(condition.get("op", "eq")).casefold()
    expected = condition.get("value")
    actual = get_field(record, field)

    an = _num(actual)
    if op == "eq":
        en = _num(expected)
        if an is not None and en is not None and abs(an - en) <= 1:
            return 0.5
        if actual is not None and expected is not None:
            a, e = _norm(actual), _norm(expected)
            if a and e and (a in e or e in a):
                return 0.5

    if op == "range" and isinstance(expected, list) and len(expected) == 2 and an is not None:
        low, high = _num(expected[0]), _num(expected[1])
        if low is not None and high is not None:
            margin = max(1.0, (high - low) * 0.2)
            if low - margin <= an <= high + margin:
                return 0.5

    if op in {"lte", "gte"} and an is not None:
        en = _num(expected)
        if en is not None:
            margin = max(1.0, abs(en) * 0.1)
            if op == "lte" and an <= en + margin:
                return 0.5
            if op == "gte" and an >= en - margin:
                return 0.5

    return 0.0


def priority_weights(request: dict) -> dict[str, int]:
    result: dict[str, int] = {}
    mapping = {"high": 3, "medium": 2, "low": 1}
    for item in request.get("priority", []) or []:
        field = str(item.get("field", "")).casefold()
        level = str(item.get("level", "medium")).casefold()
        if field:
            result[field] = mapping.get(level, 2)
    return result


def score_soft_conditions(record: dict, request: dict) -> tuple[float | None, int, int]:
    conditions = request.get("soft_conditions", []) or []
    if not conditions:
        return None, 0, 0

    weights = priority_weights(request)
    numerator = 0.0
    denominator = 0.0
    high_full = 0
    medium_full = 0

    for cond in conditions:
        field = str(cond.get("field", "")).casefold()
        weight = weights.get(field, 2)
        value = soft_match_value(record, cond)
        numerator += weight * value
        denominator += weight
        if value == 1.0:
            if weight == 3:
                high_full += 1
            elif weight == 2:
                medium_full += 1

    score = 100.0 * numerator / denominator if denominator else None
    return score, high_full, medium_full


def _priority_goal_items(request: dict) -> list[dict]:
    mapping = {"high": 3, "medium": 2, "low": 1}
    result: list[dict] = []
    for item in request.get("priority", []) or []:
        field = str(item.get("field", "")).strip()
        level = str(item.get("level", "medium")).casefold()
        goal = str(item.get("goal", "")).casefold()
        if field and goal in {"min", "max"}:
            result.append(
                {
                    "field": field,
                    "level": level,
                    "weight": mapping.get(level, 2),
                    "goal": goal,
                }
            )
    return result


def relative_preference_value(record: dict, preference: dict, candidate_records: list[dict]) -> float:
    current = _num(get_field(record, preference["field"]))
    if current is None:
        return 0.0

    values = [
        value
        for candidate in candidate_records
        if (value := _num(get_field(candidate, preference["field"]))) is not None
    ]
    if not values:
        return 0.0

    low, high = min(values), max(values)
    if math.isclose(low, high, rel_tol=1e-9, abs_tol=1e-9):
        return 1.0

    position = (current - low) / (high - low)
    if preference["goal"] == "min":
        return max(0.0, min(1.0, 1.0 - position))
    return max(0.0, min(1.0, position))


def score_request(
    record: dict,
    request: dict,
    candidate_records: list[dict],
) -> tuple[float | None, int, int, list[dict]]:
    weights = priority_weights(request)
    numerator = 0.0
    denominator = 0.0
    high_full = 0
    medium_full = 0
    details: list[dict] = []

    for cond in request.get("soft_conditions", []) or []:
        field = str(cond.get("field", "")).casefold()
        weight = weights.get(field, 2)
        value = soft_match_value(record, cond)
        numerator += weight * value
        denominator += weight
        if value == 1.0:
            if weight == 3:
                high_full += 1
            elif weight == 2:
                medium_full += 1

    for pref in _priority_goal_items(request):
        value = relative_preference_value(record, pref, candidate_records)
        weight = pref["weight"]
        numerator += weight * value
        denominator += weight
        if value >= 0.95:
            if weight == 3:
                high_full += 1
            elif weight == 2:
                medium_full += 1
        details.append(
            {
                "field": pref["field"],
                "goal": pref["goal"],
                "level": pref["level"],
                "score": value,
            }
        )

    score = 100.0 * numerator / denominator if denominator else None
    return score, high_full, medium_full, details


def stars_from_score(score: float | None, exact_match: bool) -> int | None:
    if score is None:
        return None
    if not exact_match:
        return min(2, 2 if score >= 40 else 1)
    if score >= 90:
        return 5
    if score >= 75:
        return 4
    if score >= 60:
        return 3
    if score >= 40:
        return 2
    return 1


def describe_condition(condition: dict) -> str:
    return f"{condition.get('field')} {condition.get('op', 'eq')} {condition.get('value')}"


def condition_summary(record: dict, request: dict) -> tuple[list[str], list[str]]:
    reasons: list[str] = []
    unmet: list[str] = []

    for cond in request.get("hard_conditions", []) or []:
        text = describe_condition(cond)
        if condition_match(record, cond):
            reasons.append(text)
        else:
            unmet.append(text)

    for cond in request.get("soft_conditions", []) or []:
        value = soft_match_value(record, cond)
        text = describe_condition(cond)
        if value == 1:
            reasons.append(text)
        elif value == 0:
            unmet.append(text)

    return reasons, unmet


def preference_summary(preference_details: list[dict]) -> list[str]:
    reasons: list[str] = []
    for item in preference_details:
        if item["score"] < 0.5:
            continue
        direction = "越低越好" if item["goal"] == "min" else "越高越好"
        reasons.append(f"{item['field']} {direction}（{item['level']}优先级）")
    return reasons
