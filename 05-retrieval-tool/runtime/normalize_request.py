from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_OPS = {"eq", "neq", "contains", "lte", "gte", "lt", "gt", "range", "in"}
ALLOWED_LEVELS = {"high", "medium", "low"}
ALLOWED_GOALS = {"min", "max"}


def _load_json(args) -> dict[str, Any]:
    if args.request_json:
        data = json.loads(args.request_json)
    elif args.request_file:
        data = json.loads(Path(args.request_file).read_text(encoding="utf-8"))
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("缺少 Search_Request JSON")
        data = json.loads(raw)

    if not isinstance(data, dict):
        raise ValueError("Search_Request 必须是 JSON object")
    return data


def _normalize_condition(item: Any, group: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError(f"{group} 中每一项必须是 object")

    field = str(item.get("field", "")).strip()
    op = str(item.get("op", "eq")).casefold().strip()
    if not field:
        raise ValueError(f"{group} 条件缺少 field")
    if op not in ALLOWED_OPS:
        raise ValueError(f"{group} 不支持 op={op}")
    if "value" not in item:
        raise ValueError(f"{group} 条件缺少 value")

    return {
        "field": field,
        "op": op,
        "value": item.get("value"),
    }


def _normalize_priority(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("priority 中每一项必须是 object")

    field = str(item.get("field", "")).strip()
    level = str(item.get("level", "medium")).casefold().strip()
    goal_raw = item.get("goal")
    goal = str(goal_raw).casefold().strip() if goal_raw is not None else None

    if not field:
        raise ValueError("priority 缺少 field")
    if level not in ALLOWED_LEVELS:
        raise ValueError(f"priority 不支持 level={level}")
    if goal is not None and goal not in ALLOWED_GOALS:
        raise ValueError(f"priority 不支持 goal={goal}")

    result: dict[str, Any] = {
        "field": field,
        "level": level,
    }
    if goal:
        result["goal"] = goal
    return result


def normalize_request(data: dict[str, Any]) -> dict[str, Any]:
    category = data.get("product_category")
    category = str(category).strip() if category is not None else None
    if category == "":
        category = None

    hard = [
        _normalize_condition(item, "hard_conditions")
        for item in (data.get("hard_conditions") or [])
    ]
    soft = [
        _normalize_condition(item, "soft_conditions")
        for item in (data.get("soft_conditions") or [])
    ]
    priority = [
        _normalize_priority(item)
        for item in (data.get("priority") or [])
    ]

    semantic = str(data.get("semantic_query") or "").strip()

    return {
        "product_category": category,
        "hard_conditions": hard,
        "soft_conditions": soft,
        "priority": priority,
        "semantic_query": semantic,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="校验并标准化 Search_Request JSON")
    parser.add_argument("--request-json")
    parser.add_argument("--request-file")
    args = parser.parse_args()

    try:
        normalized = normalize_request(_load_json(args))
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
