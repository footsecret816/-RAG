from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import (
    ALLOWED_FUNCTION_TAGS,
    ALLOWED_MATERIALS,
    ALLOWED_SCENARIO_TAGS,
    ALLOWED_SIZE_SYSTEMS,
    ALLOWED_SPECIAL_FEATURES,
    PERFORMANCE_RULES,
)


def validate_product(product: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sku = str(product.get("SKU_ID") or "").strip()
    category = str(product.get("Product_Category") or "").strip()

    if not sku:
        errors.append("SKU_ID 不能为空")
    if not category:
        errors.append(f"{sku or '?'}: Product_Category 不能为空")

    for tag in product.get("Function_Tags") or []:
        if tag not in ALLOWED_FUNCTION_TAGS:
            errors.append(f"{sku}: Function_Tags 非标准值：{tag}")

    for tag in product.get("Scenario_Tags") or []:
        if tag not in ALLOWED_SCENARIO_TAGS:
            errors.append(f"{sku}: Scenario_Tags 非标准值：{tag}")

    for tag in product.get("Special_Features") or []:
        if tag not in ALLOWED_SPECIAL_FEATURES:
            errors.append(f"{sku}: Special_Features 非标准值：{tag}")

    perf = product.get("Performance_Attributes") or {}
    for key, rule in PERFORMANCE_RULES.items():
        value = perf.get(key)
        if value in (None, ""):
            continue

        rule_type = str(rule.get("type") or "").casefold()
        if rule_type == "number":
            try:
                num = float(value)
            except (TypeError, ValueError):
                errors.append(f"{sku}: {key} 必须为数值")
                continue

            minimum = rule.get("min")
            maximum = rule.get("max")
            if minimum is not None and num < float(minimum):
                errors.append(f"{sku}: {key} 低于允许范围")
            if maximum is not None and num > float(maximum):
                errors.append(f"{sku}: {key} 超出允许范围")

        elif rule_type == "enum":
            allowed = set(rule.get("allowed") or [])
            if value not in allowed:
                errors.append(f"{sku}: {key} 非标准值：{value}")

    offers = product.get("Factory_Offers") or []
    if not offers:
        errors.append(f"{sku}: Factory_Offers 至少需要一条")

    factories: set[str] = set()
    for offer in offers:
        factory = str(offer.get("Factory_Name") or "").strip()
        if not factory:
            errors.append(f"{sku}: Factory_Name 不能为空")
            continue
        key = factory.casefold()
        if key in factories:
            errors.append(f"{sku}: Factory_Name 重复：{factory}")
        factories.add(key)

        material = offer.get("Material")
        if material not in (None, "") and material not in ALLOWED_MATERIALS:
            errors.append(f"{sku}/{factory}: Material 非标准值：{material}")

        size_system = offer.get("Size_System")
        if size_system not in (None, "") and size_system not in ALLOWED_SIZE_SYSTEMS:
            errors.append(f"{sku}/{factory}: Size_System 非标准值：{size_system}")

        for number_field in ("Price", "MOQ"):
            value = offer.get(number_field)
            if value not in (None, "") and not isinstance(value, (int, float)):
                errors.append(f"{sku}/{factory}: {number_field} 必须为数值")

        price_term = offer.get("Price_Term")
        if price_term not in (None, ""):
            if not isinstance(price_term, str):
                errors.append(f"{sku}/{factory}: Price_Term 必须为文本或 null")
            elif not price_term.strip():
                errors.append(
                    f"{sku}/{factory}: Price_Term 不得为空白字符（空白不得覆盖旧值）"
                )

    for item in product.get("Review_Items") or []:
        if item.get("status") not in {"confirmed", "missing_optional", "removed"}:
            errors.append(
                f"{sku}: REVIEW 未完成：{item.get('id') or item.get('field')}"
            )

    return errors


def validate_candidate(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    blocking_issues = [
        issue for issue in data.get("issues", [])
        if issue.get("type") == "blocking"
    ]
    for issue in blocking_issues:
        errors.append(
            f"原始导入阻塞问题 row={issue.get('row')}: {issue.get('message')}"
        )

    products = data.get("products")
    if not isinstance(products, list) or not products:
        errors.append("candidate.products 必须是非空列表")
        products = []

    seen: set[str] = set()
    for product in products:
        sku = str(product.get("SKU_ID") or "").strip()
        if sku.casefold() in seen and sku:
            errors.append(f"candidate 中 SKU 重复：{sku}")
        seen.add(sku.casefold())
        errors.extend(validate_product(product))

    return {
        "ok": not errors,
        "errors": errors,
        "product_count": len(products),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 03 候选数据")
    parser.add_argument("candidate")
    args = parser.parse_args()

    path = Path(args.candidate).expanduser().resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    result = validate_candidate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
