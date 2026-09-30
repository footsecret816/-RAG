from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml

from config import PRODUCT_PREFIX


_SPLIT_RE = re.compile(r"[\s,，;；/|、+]+")
_PERFORMANCE_LABELS = {
    "Cushioning": "缓震",
    "Elasticity": "回弹",
    "Softness": "软硬",
    "Arch_Height": "足弓高度",
    "Arch_Support": "足弓支撑",
    "Heel_Cup_Depth": "后跟杯深度",
}


def _front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        raise ValueError("product.md 缺少 YAML front matter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("product.md YAML front matter 未正确闭合")
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        raise ValueError("product.md front matter 必须是对象")
    return data


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean(v) for v in value if _clean(v)]
    text = _clean(value)
    return [text] if text else []


def _record_id(sku: str, factory: str) -> str:
    raw = f"{sku}::{factory}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:20]


def _semantic_body(product: dict[str, Any], offer: dict[str, Any]) -> str:
    parts: list[str] = []

    category = _clean(product.get("Product_Category"))
    if category:
        parts.append(f"品类：{category}")

    material = _clean(offer.get("Material"))
    if material:
        parts.append(f"材质：{material}")

    detail = _clean(offer.get("Material_Detail"))
    if detail:
        parts.append(f"结构与材质细节：{detail}")

    function_tags = _list(product.get("Function_Tags"))
    if function_tags:
        parts.append("核心功能：" + "、".join(function_tags))

    performance = product.get("Performance_Attributes") or {}
    perf_items: list[str] = []
    if isinstance(performance, dict):
        for key, label in _PERFORMANCE_LABELS.items():
            value = performance.get(key)
            if value is not None and _clean(value):
                perf_items.append(f"{label}{_clean(value)}")
    if perf_items:
        parts.append("性能：" + "、".join(perf_items))

    scenario_tags = _list(product.get("Scenario_Tags"))
    if scenario_tags:
        parts.append("适用场景：" + "、".join(scenario_tags))

    special = _list(product.get("Special_Features"))
    if special:
        parts.append("特殊属性：" + "、".join(special))

    return "；".join(parts)


def _keywords(product: dict[str, Any], offer: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("Function_Tags", "Scenario_Tags", "Special_Features"):
        values.extend(_list(product.get(key)))

    material = _clean(offer.get("Material"))
    detail = _clean(offer.get("Material_Detail"))
    if material:
        values.append(material)
    if detail:
        values.extend([x for x in _SPLIT_RE.split(detail) if len(x) >= 2])

    perf = product.get("Performance_Attributes") or {}
    if isinstance(perf, dict):
        for key, label in _PERFORMANCE_LABELS.items():
            value = perf.get(key)
            if value is not None and _clean(value):
                values.extend([label, f"{label}{_clean(value)}"])

    category = _clean(product.get("Product_Category"))
    if category:
        values.append(category)

    seen: set[str] = set()
    result: list[str] = []
    for item in values:
        norm = item.casefold().strip()
        if norm and norm not in seen:
            seen.add(norm)
            result.append(item.strip())
    return result


def load_product_file(path: Path, product_data_root: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    product = _front_matter(text)

    sku = _clean(product.get("SKU_ID"))
    category = _clean(product.get("Product_Category"))
    if not sku:
        raise ValueError(f"{path}: SKU_ID 不能为空")
    if not category:
        raise ValueError(f"{path}: Product_Category 不能为空")

    main_image = _clean(product.get("Main_Image")) or "main.jpg"
    image_path = (path.parent / main_image).resolve()
    try:
        image_ref = image_path.relative_to(product_data_root.resolve()).as_posix()
    except ValueError:
        image_ref = str(image_path)

    offers = product.get("Factory_Offers") or []
    if not isinstance(offers, list) or not offers:
        raise ValueError(f"{path}: Factory_Offers 至少需要一条")

    records: list[dict[str, Any]] = []
    for offer in offers:
        if not isinstance(offer, dict):
            continue
        factory = _clean(offer.get("Factory_Name"))
        if not factory:
            raise ValueError(f"{path}: Factory_Name 不能为空")

        body = _semantic_body(product, offer)
        records.append(
            {
                "record_id": _record_id(sku, factory),
                "product_sku": sku,
                "product_category": category,
                "source_file": path.resolve().as_posix(),
                "product": {
                    "main_image": image_ref,
                    "function_tags": _list(product.get("Function_Tags")),
                    "scenario_tags": _list(product.get("Scenario_Tags")),
                    "special_features": _list(product.get("Special_Features")),
                    "performance_attributes": product.get("Performance_Attributes") or {},
                },
                "factory_offer": {
                    "factory_name": factory,
                    "material": offer.get("Material"),
                    "material_detail": offer.get("Material_Detail"),
                    "price": offer.get("Price"),
                    "moq": offer.get("MOQ"),
                    "size_system": offer.get("Size_System"),
                    "size_range": offer.get("Size_Range"),
                },
                "packaging_options": _list(product.get("Packaging_Options")),
                "keywords": _keywords(product, offer),
                "semantic_body": body,
                "semantic_text": PRODUCT_PREFIX + body,
            }
        )

    return records


def load_all_records(product_kb_dir: Path, product_data_root: Path) -> list[dict[str, Any]]:
    if not product_kb_dir.exists():
        raise FileNotFoundError(f"Product_KB 不存在：{product_kb_dir}")

    records: list[dict[str, Any]] = []
    errors: list[str] = []

    for path in sorted(product_kb_dir.rglob("product.md")):
        try:
            records.extend(load_product_file(path, product_data_root))
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    if errors:
        raise ValueError("产品资料读取失败：\n" + "\n".join(errors))

    if not records:
        raise ValueError(f"Product_KB 中没有找到有效 product.md：{product_kb_dir}")

    ids = [r["record_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("存在重复的 SKU_ID + Factory_Name，无法建立唯一检索记录")

    return records
