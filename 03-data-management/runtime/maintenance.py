from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    PERFORMANCE_KEYS,
    category_dir,
    dump_product_md,
    is_blank,
    parse_product_md,
    product_data_root,
    write_json,
)
from validate_candidate import validate_candidate


PRODUCT_LIST_FIELDS = (
    "Packaging_Options",
    "Function_Tags",
    "Scenario_Tags",
    "Special_Features",
)
FACTORY_FIELDS = (
    "Material",
    "Material_Detail",
    "Price",
    "MOQ",
    "Size_System",
    "Size_Range",
)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _blank_product(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "Product_Category": candidate.get("Product_Category"),
        "SKU_ID": candidate.get("SKU_ID"),
        "Main_Image": "main.jpg",
        "Packaging_Options": [],
        "Function_Tags": [],
        "Scenario_Tags": [],
        "Special_Features": [],
        "Performance_Attributes": {key: None for key in PERFORMANCE_KEYS},
        "Factory_Offers": [],
    }


def _merge_candidate(
    old: dict[str, Any] | None,
    candidate: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sku = str(candidate.get("SKU_ID"))
    result = _blank_product(candidate) if old is None else json.loads(json.dumps(old, ensure_ascii=False))
    changes: list[dict[str, Any]] = []

    if old is None:
        changes.append({
            "product_sku": sku,
            "change_type": "new_sku",
            "factory_name": None,
            "changed_fields": ["Product_Category", "SKU_ID"],
        })

    category = candidate.get("Product_Category")
    if not is_blank(category) and result.get("Product_Category") != category:
        before = result.get("Product_Category")
        result["Product_Category"] = category
        changes.append({
            "product_sku": sku,
            "change_type": "update",
            "factory_name": None,
            "changed_fields": ["Product_Category"],
            "before": {"Product_Category": before},
            "after": {"Product_Category": category},
        })

    for field in PRODUCT_LIST_FIELDS:
        value = candidate.get(field)
        if value:
            if result.get(field) != value:
                before = result.get(field)
                result[field] = value
                changes.append({
                    "product_sku": sku,
                    "change_type": "update",
                    "factory_name": None,
                    "changed_fields": [field],
                    "before": {field: before},
                    "after": {field: value},
                })

    cand_perf = candidate.get("Performance_Attributes") or {}
    result_perf = result.setdefault("Performance_Attributes", {})
    perf_changed: list[str] = []
    perf_before: dict[str, Any] = {}
    perf_after: dict[str, Any] = {}
    for field in PERFORMANCE_KEYS:
        value = cand_perf.get(field)
        if is_blank(value):
            continue
        if result_perf.get(field) != value:
            perf_before[field] = result_perf.get(field)
            result_perf[field] = value
            perf_after[field] = value
            perf_changed.append(field)
    if perf_changed:
        changes.append({
            "product_sku": sku,
            "change_type": "update",
            "factory_name": None,
            "changed_fields": perf_changed,
            "before": perf_before,
            "after": perf_after,
        })

    existing_offers = {
        str(x.get("Factory_Name") or "").strip(): x
        for x in result.get("Factory_Offers", [])
        if str(x.get("Factory_Name") or "").strip()
    }

    for cand_offer in candidate.get("Factory_Offers") or []:
        factory = str(cand_offer.get("Factory_Name") or "").strip()
        old_offer = existing_offers.get(factory)
        if old_offer is None:
            new_offer = {
                "Factory_Name": factory,
                **{field: cand_offer.get(field) for field in FACTORY_FIELDS},
            }
            result.setdefault("Factory_Offers", []).append(new_offer)
            existing_offers[factory] = new_offer
            changes.append({
                "product_sku": sku,
                "change_type": "new_factory_offer",
                "factory_name": factory,
                "changed_fields": ["Factory_Name", *FACTORY_FIELDS],
            })
            continue

        changed_fields: list[str] = []
        before: dict[str, Any] = {}
        after: dict[str, Any] = {}
        for field in FACTORY_FIELDS:
            value = cand_offer.get(field)
            if is_blank(value):
                continue
            if old_offer.get(field) != value:
                before[field] = old_offer.get(field)
                old_offer[field] = value
                after[field] = value
                changed_fields.append(field)

        if changed_fields:
            changes.append({
                "product_sku": sku,
                "change_type": "update",
                "factory_name": factory,
                "changed_fields": changed_fields,
                "before": before,
                "after": after,
            })

    return result, changes


def _product_location(root: Path, candidate: dict[str, Any]) -> tuple[Path, Path]:
    category = str(candidate.get("Product_Category") or "").strip()
    folder = category_dir(category)
    if not folder:
        raise ValueError(f"V1 未配置 Product_Category 目录映射：{category}")
    sku_dir = root / "Product_KB" / folder / str(candidate["SKU_ID"])
    return sku_dir, sku_dir / "product.md"


def build_plan(candidate_data: dict[str, Any]) -> dict[str, Any]:
    validation = validate_candidate(candidate_data)
    if not validation["ok"]:
        return {"ok": False, "validation": validation, "changes": []}

    root = product_data_root()
    all_changes: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []

    for candidate in candidate_data["products"]:
        sku_dir, md_path = _product_location(root, candidate)
        old = parse_product_md(md_path) if md_path.exists() else None
        merged, changes = _merge_candidate(old, candidate)

        image_source = candidate.get("Main_Image_Source")
        image_change = None
        if image_source:
            source = Path(image_source).expanduser().resolve()
            if not source.exists():
                raise FileNotFoundError(f"{candidate['SKU_ID']}: 主图不存在：{source}")
            target_name = "main" + source.suffix.casefold()
            target = sku_dir / target_name
            if _sha256(source) != _sha256(target):
                image_change = {
                    "product_sku": candidate["SKU_ID"],
                    "change_type": "image_update",
                    "factory_name": None,
                    "changed_fields": ["Main_Image"],
                    "source": str(source),
                    "target": str(target),
                }
                changes.append(image_change)
            merged["Main_Image"] = target_name
        elif old is not None:
            merged["Main_Image"] = old.get("Main_Image") or "main.jpg"

        all_changes.extend(changes)
        products.append({
            "sku": candidate["SKU_ID"],
            "sku_dir": str(sku_dir),
            "product_md": str(md_path),
            "exists": old is not None,
            "merged": merged,
            "image_change": image_change,
            "changes": changes,
        })

    return {
        "ok": True,
        "validation": validation,
        "change_count": len(all_changes),
        "changes": all_changes,
        "products": products,
    }


def commit_plan(plan: dict[str, Any], update_index: bool = False) -> dict[str, Any]:
    if not plan.get("ok"):
        raise ValueError("plan 未通过校验，禁止写入")

    root = product_data_root()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = root / "_Staging" / "backups" / stamp

    for item in plan["products"]:
        sku_dir = Path(item["sku_dir"])
        md_path = Path(item["product_md"])
        sku_dir.mkdir(parents=True, exist_ok=True)

        if md_path.exists():
            dst = backup_root / item["sku"] / "product.md"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_path, dst)

        old_image = None
        if md_path.exists():
            try:
                old_data = parse_product_md(md_path)
                old_image = old_data.get("Main_Image")
            except Exception:
                old_image = None
        if old_image:
            old_image_path = sku_dir / str(old_image)
            if old_image_path.exists():
                dst = backup_root / item["sku"] / old_image_path.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(old_image_path, dst)

        _atomic_write(md_path, dump_product_md(item["merged"]))

        image_change = item.get("image_change")
        if image_change:
            source = Path(image_change["source"])
            target = Path(image_change["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    change_set_path = root / "_Staging" / f"change-set-{stamp}.json"
    write_json(change_set_path, {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "changes": plan["changes"],
    })

    index_result = None
    if update_index and plan["changes"]:
        repo_root = Path(__file__).resolve().parents[2]
        update_script = repo_root / "04-search" / "runtime" / "update_index.py"
        proc = subprocess.run(
            [sys.executable, str(update_script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        index_result = {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
        if proc.returncode != 0:
            raise RuntimeError(
                "Product_KB 已写入，但 update_index.py 失败。"
                f"\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
            )

    return {
        "ok": True,
        "committed_change_count": len(plan["changes"]),
        "change_set": str(change_set_path),
        "backup_root": str(backup_root),
        "index_update": index_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="03 产品候选差异预览 / 安全提交")
    parser.add_argument("candidate")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="与 --commit 同时使用，表示操作者已经明确确认本次变更",
    )
    parser.add_argument("--update-index", action="store_true")
    args = parser.parse_args()

    candidate_path = Path(args.candidate).expanduser().resolve()
    data = json.loads(candidate_path.read_text(encoding="utf-8"))
    plan = build_plan(data)

    if not args.commit:
        printable = {
            "ok": plan.get("ok"),
            "validation": plan.get("validation"),
            "change_count": plan.get("change_count", 0),
            "changes": plan.get("changes", []),
        }
        print(json.dumps(printable, ensure_ascii=False, indent=2))
        return 0 if plan.get("ok") else 2

    if not args.confirm:
        print(json.dumps({
            "ok": False,
            "error": "--commit 必须同时提供 --confirm；禁止未经明确确认写入 Product_KB",
        }, ensure_ascii=False, indent=2))
        return 2

    if not plan.get("ok"):
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 2

    result = commit_plan(plan, update_index=args.update_index)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
