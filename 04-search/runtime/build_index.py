from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from config import (
    INDEX_SCHEMA_VERSION,
    MODEL_DIMENSION,
    MODEL_ID,
    SEMANTIC_TEMPLATE_VERSION,
    SIMILARITY,
    get_config,
)
from embedder import EmbeddingRuntime
from index_store import paths, save_index
from io_utils import write_json
from product_loader import load_all_records
from validate_index import validate_index


def build_index() -> dict:
    cfg = get_config()
    records = load_all_records(cfg.product_kb_dir, cfg.product_data_root)

    embedder = EmbeddingRuntime(cfg)
    embeddings = embedder.encode_products([r["semantic_body"] for r in records])

    now = datetime.now(timezone.utc).isoformat()
    meta = {
        "status": "building",
        "index_version": INDEX_SCHEMA_VERSION,
        "semantic_template_version": SEMANTIC_TEMPLATE_VERSION,
        "embedding_model": MODEL_ID,
        "embedding_model_source": cfg.model_source,
        "embedding_model_revision": cfg.model_revision,
        "dimension": MODEL_DIMENSION,
        "similarity": SIMILARITY,
        "record_count": len(records),
        "generated_at": now,
        "updated_at": now,
    }
    save_index(cfg, records, embeddings, meta)

    validation = validate_index()
    meta["status"] = "normal" if validation["ok"] else "abnormal"
    meta["validation"] = {
        "ok": validation["ok"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(paths(cfg)["meta"], meta)

    return {
        "ok": validation["ok"],
        "record_count": len(records),
        "model": MODEL_ID,
        "dimension": MODEL_DIMENSION,
        "index_dir": str(cfg.search_index_dir),
        "validation": validation["checks"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="从 Product_KB 首次建立混合检索索引")
    parser.parse_args()
    result = build_index()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
