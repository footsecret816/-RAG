from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml


MATERIAL_ALIASES = {
    "memory foam": "记忆棉",
    "memory sponge": "记忆棉",
    "慢回弹海绵": "记忆棉",
    "慢回弹泡棉": "记忆棉",
    "记忆棉": "记忆棉",
    "polyurethane": "PU",
    "聚氨酯": "PU",
    "pu foam": "PU",
    "pu": "PU",
    "eva": "EVA",
    "gel": "Gel",
    "poron": "PORON",
    "latex": "乳胶",
    "乳胶": "乳胶",
    "haipoli": "Haipoli",
    "海波丽": "Haipoli",
    "tpu": "TPU",
    "tpe": "TPE",
    "pe foam": "PE Foam",
    "pe": "PE Foam",
}

ALLOWED_MATERIALS = {
    "记忆棉", "PU", "EVA", "Gel", "PORON", "乳胶",
    "Haipoli", "TPU", "TPE", "PE Foam",
}
ALLOWED_FUNCTION_TAGS = {
    "足弓支撑", "缓震", "回弹", "抗疲劳减压", "防滑", "透气排湿", "防臭",
}
ALLOWED_SCENARIO_TAGS = {
    "日常", "长距离行走", "长时间站立", "长时间站立 / 工作", "长时间站立/工作",
    "劳保 / 安全鞋", "劳保/安全鞋", "跑步", "篮球", "足球", "健身 / 训练",
    "健身/训练", "综合运动", "户外徒步", "登山 / 越野", "登山/越野",
    "休闲 / 皮鞋", "休闲/皮鞋", "紧脚鞋",
}
ALLOWED_SPECIAL_FEATURES = {"防穿刺", "防静电", "ESD", "绝缘"}
ALLOWED_SIZE_SYSTEMS = {"EU", "US", "UK", "Alpha"}

PERFORMANCE_KEYS = (
    "Cushioning",
    "Elasticity",
    "Softness",
    "Arch_Height",
    "Arch_Support",
    "Heel_Cup_Depth",
)
ALLOWED_ARCH_HEIGHT = {"低", "中", "高", "low", "medium", "high"}
ALLOWED_ARCH_SUPPORT = {
    "无支撑", "轻度支撑", "强支撑", "no", "light", "strong",
}
ALLOWED_HEEL_CUP = {
    "平", "浅", "中", "深", "flat", "shallow", "medium", "deep",
}

CATEGORY_DIRS = {
    "鞋垫": "insoles",
    "insole": "insoles",
    "insoles": "insoles",
}


def product_data_root() -> Path:
    value = os.getenv("RUNTONG_PRODUCT_DATA")
    if value:
        return Path(value).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for candidate in (
        cwd / "RUNTONG products" / "Product_Data",
        cwd / "Product_Data",
        cwd.parent / "RUNTONG products" / "Product_Data",
        cwd.parent / "Product_Data",
    ):
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(
        "未找到 Product_Data。请设置 RUNTONG_PRODUCT_DATA。"
    )


def text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def is_blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip()) or value == []


def parse_number(value: Any) -> int | float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        num = float(value)
    else:
        cleaned = text(value).replace(",", "")
        match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
        if not match:
            return None
        num = float(match.group())
    return int(num) if num.is_integer() else num


def split_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        values = value
    else:
        values = re.split(r"[,，;；|、\n]+", text(value))
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        item = text(item)
        if not item:
            continue
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def normalize_material(value: Any) -> str | None:
    raw = text(value)
    if not raw:
        return None
    if raw in ALLOWED_MATERIALS:
        return raw
    mapped = MATERIAL_ALIASES.get(raw.casefold())
    return mapped


def normalize_size_system(value: Any) -> str | None:
    raw = text(value)
    if not raw:
        return None
    lookup = {
        "eu": "EU", "欧码": "EU",
        "us": "US", "美码": "US",
        "uk": "UK", "英码": "UK",
        "alpha": "Alpha", "字母": "Alpha", "字母尺码": "Alpha",
    }
    return lookup.get(raw.casefold())


def category_dir(category: str) -> str:
    return CATEGORY_DIRS.get(category.casefold(), CATEGORY_DIRS.get(category, ""))


def parse_product_md(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"{path}: product.md 缺少 YAML front matter")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: YAML front matter 未闭合")
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: YAML front matter 必须为 object")
    return data


def dump_product_md(data: dict[str, Any]) -> str:
    ordered = {
        "Product_Category": data.get("Product_Category"),
        "SKU_ID": data.get("SKU_ID"),
        "Main_Image": data.get("Main_Image") or "main.jpg",
        "Packaging_Options": data.get("Packaging_Options") or [],
        "Function_Tags": data.get("Function_Tags") or [],
        "Scenario_Tags": data.get("Scenario_Tags") or [],
        "Special_Features": data.get("Special_Features") or [],
        "Performance_Attributes": {
            key: (data.get("Performance_Attributes") or {}).get(key)
            for key in PERFORMANCE_KEYS
        },
        "Factory_Offers": data.get("Factory_Offers") or [],
    }
    body = yaml.safe_dump(
        ordered,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return f"---\n{body}---\n"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
