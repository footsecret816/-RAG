from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from profiles.profile_loader import (
    default_product_category,
    load_company_profile,
    load_default_product_profile,
)


_PRODUCT_PROFILE = load_default_product_profile()
_CATEGORY = _PRODUCT_PROFILE.get("product_category") or {}
_MATERIALS = _PRODUCT_PROFILE.get("materials") or {}
_SIZE_SYSTEMS = _PRODUCT_PROFILE.get("size_systems") or {}
_TAGS = _PRODUCT_PROFILE.get("tags") or {}

MATERIAL_ALIASES = {
    str(key).casefold(): str(value)
    for key, value in (_MATERIALS.get("aliases") or {}).items()
}
ALLOWED_MATERIALS = set(_MATERIALS.get("allowed") or [])
ALLOWED_FUNCTION_TAGS = set(_TAGS.get("function") or [])
ALLOWED_SCENARIO_TAGS = set(_TAGS.get("scenario") or [])
ALLOWED_SPECIAL_FEATURES = set(_TAGS.get("special") or [])

ALLOWED_SIZE_SYSTEMS = set(_SIZE_SYSTEMS.get("allowed") or [])
SIZE_SYSTEM_ALIASES = {
    str(key).casefold(): str(value)
    for key, value in (_SIZE_SYSTEMS.get("aliases") or {}).items()
}

PERFORMANCE_RULES = _PRODUCT_PROFILE.get("performance_attributes") or {}
PERFORMANCE_KEYS = tuple(PERFORMANCE_RULES.keys())
PERFORMANCE_LABELS = {
    key: str(rule.get("label") or key)
    for key, rule in PERFORMANCE_RULES.items()
}
PERFORMANCE_COLUMN_ALIASES = {
    key: [str(x) for x in (rule.get("column_aliases") or [key])]
    for key, rule in PERFORMANCE_RULES.items()
}
NUMERIC_PERFORMANCE_KEYS = tuple(
    key
    for key, rule in PERFORMANCE_RULES.items()
    if str(rule.get("type") or "").casefold() == "number"
)
ENUM_PERFORMANCE_KEYS = tuple(
    key
    for key, rule in PERFORMANCE_RULES.items()
    if str(rule.get("type") or "").casefold() == "enum"
)

DEFAULT_PRODUCT_CATEGORY = default_product_category()
_CATEGORY_DIR = str(_CATEGORY.get("directory") or "").strip()
CATEGORY_DIRS = {
    str(alias).casefold(): _CATEGORY_DIR
    for alias in (_CATEGORY.get("aliases") or [DEFAULT_PRODUCT_CATEGORY])
    if str(alias).strip()
}


def _runtime_env_value(logical_name: str) -> str | None:
    runtime = load_company_profile().get("runtime") or {}
    env_spec = runtime.get(logical_name) or {}
    for key in ("legacy", "generic"):
        env_name = str(env_spec.get(key) or "").strip()
        if env_name:
            value = os.getenv(env_name)
            if value:
                return value
    return None


def product_data_root() -> Path:
    explicit = _runtime_env_value("product_data_env")
    if explicit:
        return Path(explicit).expanduser().resolve()

    runtime = load_company_profile().get("runtime") or {}
    hints = runtime.get("product_data_path_hints") or ["Product_Data"]

    cwd = Path.cwd().resolve()
    candidates: list[Path] = []
    for base in (cwd, cwd.parent):
        for hint in hints:
            candidates.append(base / str(hint))

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "未找到 Product_Data。请设置 PRODUCT_DATA_ROOT，"
        "或当前 Company Profile 中配置的兼容环境变量。"
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
    return MATERIAL_ALIASES.get(raw.casefold())


def normalize_size_system(value: Any) -> str | None:
    raw = text(value)
    if not raw:
        return None
    if raw in ALLOWED_SIZE_SYSTEMS:
        return raw
    return SIZE_SYSTEM_ALIASES.get(raw.casefold())


def category_dir(category: str) -> str:
    return CATEGORY_DIRS.get(str(category).casefold(), "")


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
