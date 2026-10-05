from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import PERFORMANCE_KEYS, write_json
from validate_candidate import validate_candidate


ALLOWED_PRODUCT_FIELDS = {
    "Product_Category",
    "Main_Image_Source",
    "Packaging_Options",
    "Function_Tags",
    "Scenario_Tags",
    "Special_Features",
}
ALLOWED_REVIEW_STATUS = {"confirmed", "missing_optional", "removed", "pending"}


def apply_patch(candidate: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    products = {
        str(p.get("SKU_ID")): p
        for p in candidate.get("products", [])
        if p.get("SKU_ID")
    }

    for sku, changes in (patch.get("products") or {}).items():
        if sku not in products:
            raise ValueError(f"候选中不存在 SKU：{sku}")
        product = products[sku]

        for field, value in (changes.get("fields") or {}).items():
            if field not in ALLOWED_PRODUCT_FIELDS:
                raise ValueError(f"不允许通过 patch 修改字段：{field}")
            product[field] = value

        perf_patch = changes.get("Performance_Attributes") or {}
        perf = product.setdefault("Performance_Attributes", {})
        for field, value in perf_patch.items():
            if field not in PERFORMANCE_KEYS:
                raise ValueError(f"未知 Performance 字段：{field}")
            perf[field] = value

        offer_patches = changes.get("Factory_Offers") or []
        for offer_patch in offer_patches:
            factory = str(offer_patch.get("Factory_Name") or "").strip()
            if not factory:
                raise ValueError(f"{sku}: Factory_Offers patch 缺少 Factory_Name")
            offer = next(
                (x for x in product.get("Factory_Offers", [])
                 if str(x.get("Factory_Name") or "").strip() == factory),
                None,
            )
            if offer is None:
                raise ValueError(f"{sku}: 候选中不存在工厂 {factory}")
            for field, value in offer_patch.items():
                if field == "Factory_Name":
                    continue
                if field not in {
                    "Material", "Material_Detail", "Price", "Price_Term", "MOQ",
                    "Size_System", "Size_Range",
                }:
                    raise ValueError(f"{sku}/{factory}: 不允许修改字段 {field}")
                offer[field] = value

        review_status = changes.get("Review_Status") or {}
        items = {
            str(item.get("id")): item
            for item in product.get("Review_Items", [])
            if item.get("id")
        }
        for review_id, status in review_status.items():
            if review_id not in items:
                raise ValueError(f"{sku}: 不存在 Review ID {review_id}")
            if status not in ALLOWED_REVIEW_STATUS:
                raise ValueError(f"{sku}: 非法 Review 状态 {status}")
            items[review_id]["status"] = status

    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="对 staging candidate 应用人工/Agent确认后的结构化 patch")
    parser.add_argument("candidate")
    parser.add_argument("patch")
    parser.add_argument("--output")
    args = parser.parse_args()

    candidate_path = Path(args.candidate).expanduser().resolve()
    patch_path = Path(args.patch).expanduser().resolve()
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    patch = json.loads(patch_path.read_text(encoding="utf-8"))

    updated = apply_patch(candidate, patch)
    validation = validate_candidate(updated)

    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else candidate_path
    )
    write_json(output, updated)

    print(json.dumps({
        "ok": validation["ok"],
        "output": str(output),
        "validation": validation,
    }, ensure_ascii=False, indent=2))
    return 0 if validation["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
