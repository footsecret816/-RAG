from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

import numpy as np

from config import (
    INDEX_SCHEMA_VERSION,
    MODEL_DIMENSION,
    MODEL_ID,
    SEMANTIC_TEMPLATE_VERSION,
    SIMILARITY,
    get_config,
)
from embedder import EmbeddingRuntime
from index_store import load_index, paths, save_index
from io_utils import write_json
from product_loader import load_all_records
from validate_index import validate_index


def update_index() -> dict:
    cfg = get_config()
    new_records = load_all_records(cfg.product_kb_dir, cfg.product_data_root)

    try:
        old_records, old_embeddings, _, old_meta = load_index(cfg)
    except FileNotFoundError:
        from build_index import build_index
        result = build_index()
        result["mode"] = "initial_build"
        return result

    if old_meta.get("embedding_model") != MODEL_ID or int(old_meta.get("dimension", -1)) != MODEL_DIMENSION:
        from build_index import build_index
        result = build_index()
        result["mode"] = "full_rebuild_model_incompatible"
        return result

    old_map = {
        r["record_id"]: (r, old_embeddings[i])
        for i, r in enumerate(old_records)
    }

    embeddings = np.empty((len(new_records), MODEL_DIMENSION), dtype=np.float32)
    to_embed_idx: list[int] = []
    to_embed_text: list[str] = []
    reused = 0

    for i, record in enumerate(new_records):
        old = old_map.get(record["record_id"])
        if old and old[0].get("semantic_text") == record.get("semantic_text"):
            embeddings[i] = old[1]
            reused += 1
        else:
            to_embed_idx.append(i)
            to_embed_text.append(record["semantic_body"])

    if to_embed_text:
        new_vectors = EmbeddingRuntime(cfg).encode_products(to_embed_text)
        for pos, vec in zip(to_embed_idx, new_vectors):
            embeddings[pos] = vec

    old_ids = {r["record_id"] for r in old_records}
    new_ids = {r["record_id"] for r in new_records}
    deleted = len(old_ids - new_ids)
    added = len(new_ids - old_ids)

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
        "record_count": len(new_records),
        "generated_at": old_meta.get("generated_at", now),
        "updated_at": now,
    }
    save_index(cfg, new_records, embeddings, meta)

    validation = validate_index()
    meta["status"] = "normal" if validation["ok"] else "abnormal"
    meta["validation"] = {
        "ok": validation["ok"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(paths(cfg)["meta"], meta)

    return {
        "ok": validation["ok"],
        "mode": "incremental_sync",
        "record_count": len(new_records),
        "reused_vectors": reused,
        "reembedded_vectors": len(to_embed_idx),
        "added_records": added,
        "deleted_records": deleted,
        "validation": validation["checks"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="同步 Product_KB 变化到检索索引")
    parser.parse_args()
    result = update_index()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
