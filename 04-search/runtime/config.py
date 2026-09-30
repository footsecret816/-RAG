from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


MODEL_ID = "intfloat/multilingual-e5-small"
MODEL_DIMENSION = 384
MODEL_FOLDER_NAME = "multilingual-e5-small"
SEMANTIC_TEMPLATE_VERSION = "v1.0"
INDEX_SCHEMA_VERSION = "v1.0"
PRODUCT_PREFIX = "passage: "
QUERY_PREFIX = "query: "
SIMILARITY = "cosine_via_normalized_inner_product"


def _env_path(name: str) -> Path | None:
    value = os.getenv(name)
    if not value:
        return None
    return Path(value).expanduser().resolve()


def discover_product_data_root() -> Path:
    explicit = _env_path("RUNTONG_PRODUCT_DATA")
    if explicit:
        return explicit

    cwd = Path.cwd().resolve()
    candidates = [
        cwd / "RUNTONG products" / "Product_Data",
        cwd / "Product_Data",
        cwd.parent / "RUNTONG products" / "Product_Data",
        cwd.parent / "Product_Data",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "未找到 Product_Data。请设置环境变量 RUNTONG_PRODUCT_DATA，"
        "例如 D:\\ACCIO\\RUNTONG products\\Product_Data"
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
    explicit_model_path = _env_path("RUNTONG_EMBEDDING_MODEL_PATH")
    local_model_dir = root / "_models" / MODEL_FOLDER_NAME

    if explicit_model_path:
        model_source = str(explicit_model_path)
    elif local_model_dir.exists() and any(local_model_dir.iterdir()):
        model_source = str(local_model_dir)
    else:
        model_source = MODEL_ID

    revision = os.getenv("RUNTONG_EMBEDDING_MODEL_REVISION") or None

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
