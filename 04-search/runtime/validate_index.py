from __future__ import annotations

import argparse
import json
from typing import Any

import numpy as np

from config import MODEL_DIMENSION, MODEL_ID, PRODUCT_PREFIX, get_config
from index_store import load_index


def validate_index() -> dict[str, Any]:
    cfg = get_config()
    records, embeddings, index, meta = load_index(cfg)

    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    add("模型名称", meta.get("embedding_model") == MODEL_ID, str(meta.get("embedding_model")))
    add("向量维度", int(meta.get("dimension", -1)) == MODEL_DIMENSION, str(meta.get("dimension")))
    add("记录数=向量数", len(records) == len(embeddings), f"{len(records)} / {len(embeddings)}")
    add("记录数=FAISS数量", len(records) == index.ntotal, f"{len(records)} / {index.ntotal}")
    add("向量为二维", embeddings.ndim == 2, str(embeddings.shape))
    add(
        "向量第二维正确",
        embeddings.ndim == 2 and embeddings.shape[1] == MODEL_DIMENSION,
        str(embeddings.shape),
    )
    add("向量无异常值", bool(np.isfinite(embeddings).all()), "")
    add("record_id唯一", len({r.get("record_id") for r in records}) == len(records), "")

    prefix_ok = all(str(r.get("semantic_text", "")).startswith(PRODUCT_PREFIX) for r in records)
    add("产品语义前缀正确", prefix_ok, PRODUCT_PREFIX)

    forbidden_hits: list[str] = []
    for r in records:
        text = str(r.get("semantic_text", ""))
        offer = r.get("factory_offer", {}) or {}
        factory_name = offer.get("factory_name")
        if factory_name and str(factory_name) in text:
            forbidden_hits.append(f"{r.get('product_sku')}:factory_name")
    add("语义文本未混入工厂名", not forbidden_hits, ",".join(forbidden_hits[:10]))

    ok = all(c["ok"] for c in checks)
    return {
        "ok": ok,
        "checks": checks,
        "meta": meta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="验证产品检索索引")
    parser.parse_args()
    result = validate_index()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
