from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from profiles.profile_loader import load_company_profile


MODEL_ID = "intfloat/multilingual-e5-small"
MODEL_DIMENSION = 384
MODEL_FOLDER_NAME = "multilingual-e5-small"
SEMANTIC_TEMPLATE_VERSION = "v1.0"
INDEX_SCHEMA_VERSION = "v1.0"
PRODUCT_PREFIX = "passage: "
QUERY_PREFIX = "query: "
SIMILARITY = "cosine_via_normalized_inner_product"


def _env_path(name: str | None) -> Path | None:
    if not name:
        return None
    value = os.getenv(name)
    if not value:
        return None
    return Path(value).expanduser().resolve()


def _runtime_env_path(logical_name: str) -> Path | None:
    runtime = load_company_profile().get("runtime") or {}
    env_spec = runtime.get(logical_name) or {}
    for key in ("legacy", "generic"):
        path = _env_path(str(env_spec.get(key) or "").strip() or None)
        if path is not None:
            return path
    return None


def _runtime_env_text(logical_name: str) -> str | None:
    runtime = load_company_profile().get("runtime") or {}
    env_spec = runtime.get(logical_name) or {}
    for key in ("generic", "legacy"):
        env_name = str(env_spec.get(key) or "").strip()
        if env_name:
            value = os.getenv(env_name)
            if value:
                return value
    return None


def discover_product_data_root() -> Path:
    explicit = _runtime_env_path("product_data_env")
    if explicit:
        return explicit

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


@dataclass(frozen=True)
class RuntimeConfig:
    product_data_root: Path
    product_kb_dir: Path
    search_index_dir: Path
    model_cache_dir: Path
    local_model_dir: Path
    model_source: str
    model_revision: str | None

    @property
    def records_dir(self) -> Path:
        return self.search_index_dir / "records"

    @property
    def keywords_dir(self) -> Path:
        return self.search_index_dir / "keywords"

    @property
    def vectors_dir(self) -> Path:
        return self.search_index_dir / "vectors"

    @property
    def meta_dir(self) -> Path:
        return self.search_index_dir / "index_meta"

    def ensure_dirs(self) -> None:
        for path in (
            self.search_index_dir,
            self.records_dir,
            self.keywords_dir,
            self.vectors_dir,
            self.meta_dir,
            self.model_cache_dir,
            self.local_model_dir.parent,
        ):
            path.mkdir(parents=True, exist_ok=True)


def get_config() -> RuntimeConfig:
    root = discover_product_data_root()
    explicit_model_path = _runtime_env_path("embedding_model_path_env")
    local_model_dir = root / "_models" / MODEL_FOLDER_NAME

    if explicit_model_path:
        model_source = str(explicit_model_path)
    elif local_model_dir.exists() and any(local_model_dir.iterdir()):
        model_source = str(local_model_dir)
    else:
        model_source = MODEL_ID

    revision = _runtime_env_text("embedding_revision_env") or None

    cfg = RuntimeConfig(
        product_data_root=root,
        product_kb_dir=root / "Product_KB",
        search_index_dir=root / "Search_Index",
        model_cache_dir=root / "_models" / "hf_cache",
        local_model_dir=local_model_dir,
        model_source=model_source,
        model_revision=revision,
    )
    cfg.ensure_dirs()
    return cfg
