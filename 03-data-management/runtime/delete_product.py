from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import dump_product_md, parse_product_md, product_data_root, write_json


def _find_sku_dir(root: Path, sku: str) -> Path:
    matches = list((root / "Product_KB").glob(f"*/{sku}"))
    matches = [p for p in matches if p.is_dir()]
    if not matches:
        raise FileNotFoundError(f"未找到 SKU：{sku}")
    if len(matches) > 1:
        raise RuntimeError(f"SKU {sku} 出现在多个分类目录，禁止自动删除")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="显式删除 SKU 或 Factory Offer")
    parser.add_argument("--sku", required=True)
    parser.add_argument("--factory")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--update-index", action="store_true")
    args = parser.parse_args()

    if not args.confirm:
        print(json.dumps({
            "ok": False,
            "error": "删除操作必须显式提供 --confirm",
        }, ensure_ascii=False, indent=2))
        return 2

    root = product_data_root()
    sku_dir = _find_sku_dir(root, args.sku)
    md_path = sku_dir / "product.md"
    data = parse_product_md(md_path)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = root / "_Staging" / "backups" / stamp / args.sku
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(sku_dir, backup)

    if args.factory:
        offers = data.get("Factory_Offers") or []
        kept = [
            x for x in offers
            if str(x.get("Factory_Name") or "").strip() != args.factory
        ]
        if len(kept) == len(offers):
            raise ValueError(f"{args.sku}: 未找到 Factory Offer：{args.factory}")
        if not kept:
            raise ValueError("不能通过删除最后一个 Factory Offer 留下空 SKU；请明确删除整个 SKU")
        data["Factory_Offers"] = kept
        md_path.write_text(dump_product_md(data), encoding="utf-8")
        change = {
            "product_sku": args.sku,
            "change_type": "delete_factory_offer",
            "factory_name": args.factory,
            "changed_fields": ["Factory_Offers"],
        }
    else:
        shutil.rmtree(sku_dir)
        change = {
            "product_sku": args.sku,
            "change_type": "delete_sku",
            "factory_name": None,
            "changed_fields": ["SKU_ID"],
        }

    change_path = root / "_Staging" / f"change-set-{stamp}-delete.json"
    write_json(change_path, {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "changes": [change],
    })

    if args.update_index:
        repo_root = Path(__file__).resolve().parents[2]
        update_script = repo_root / "04-search" / "runtime" / "update_index.py"
        proc = subprocess.run(
            [sys.executable, str(update_script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "Product_KB 删除已完成，但索引同步失败。"
                f"\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
            )

    print(json.dumps({
        "ok": True,
        "change": change,
        "backup": str(backup),
        "change_set": str(change_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
