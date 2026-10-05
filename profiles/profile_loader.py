from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


PROFILE_ROOT = Path(__file__).resolve().parent


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Profile 文件不存在：{path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Profile 必须是 YAML object：{path}")
    return data


@lru_cache(maxsize=1)
def load_active_profile() -> dict[str, Any]:
    return _read_yaml(PROFILE_ROOT / "active-profile.yaml")


@lru_cache(maxsize=1)
def load_company_profile() -> dict[str, Any]:
    active = load_active_profile()
    profile_id = str(active.get("company_profile") or "").strip()
    if not profile_id:
        raise ValueError("active-profile.yaml 缺少 company_profile")
    return _read_yaml(PROFILE_ROOT / profile_id / "company.yaml")


@lru_cache(maxsize=1)
def load_default_product_profile() -> dict[str, Any]:
    active = load_active_profile()
    company_id = str(active.get("company_profile") or "").strip()
    product_id = str(active.get("default_product_profile") or "").strip()
    if not company_id or not product_id:
        raise ValueError("active-profile.yaml 缺少 company_profile/default_product_profile")
    return _read_yaml(PROFILE_ROOT / company_id / "products" / f"{product_id}.yaml")


def default_product_category() -> str:
    profile = load_default_product_profile()
    category = profile.get("product_category") or {}
    value = str(category.get("canonical") or "").strip()
    if not value:
        raise ValueError("Product Profile 缺少 product_category.canonical")
    return value
