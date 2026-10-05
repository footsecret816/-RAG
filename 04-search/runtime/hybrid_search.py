from __future__ import annotations

from typing import Any

import numpy as np

from config import MODEL_DIMENSION, MODEL_ID, get_config
from embedder import EmbeddingRuntime
from index_store import load_index
from keyword_index import build_query_text, keyword_score
from ranking import (
    condition_match,
    condition_summary,
    preference_summary,
    score_request,
    stars_from_score,
)


def _category_match(record: dict, category: str | None) -> bool:
    if not category:
        return True
    return str(record.get("product_category", "")).casefold() == str(category).casefold()


def _hard_ok(record: dict, request: dict) -> bool:
    return all(condition_match(record, c) for c in (request.get("hard_conditions", []) or []))


def _semantic_scores(index, embedder: EmbeddingRuntime, query: str, total: int) -> dict[int, float]:
    if not query.strip() or total == 0:
        return {}
    q = embedder.encode_queries([query])
    scores, ids = index.search(np.asarray(q, dtype=np.float32), total)
    result: dict[int, float] = {}
    for idx, score in zip(ids[0].tolist(), scores[0].tolist()):
        if idx >= 0:
            result[int(idx)] = float(score)
    return result


def search(request: dict[str, Any], top_k: int = 5, debug: bool = False) -> dict[str, Any]:
    cfg = get_config()
    records, embeddings, index, meta = load_index(cfg)

    if meta.get("embedding_model") != MODEL_ID:
        raise RuntimeError(
            f"索引模型不兼容：{meta.get('embedding_model')} != {MODEL_ID}"
        )
    if int(meta.get("dimension", -1)) != MODEL_DIMENSION:
        raise RuntimeError("索引向量维度与 V1 规范不一致")
    if len(records) != len(embeddings) or index.ntotal != len(records):
        raise RuntimeError("索引记录数、向量数或 FAISS 数量不一致")

    category = request.get("product_category")
    category_pool = [i for i, r in enumerate(records) if _category_match(r, category)]
    exact_pool = [i for i in category_pool if _hard_ok(records[i], request)]

    exact_match = bool(exact_pool)
    pool = exact_pool if exact_match else category_pool
    candidate_records = [records[i] for i in pool]

    query_text = str(request.get("semantic_query") or "").strip()
    semantic_map: dict[int, float] = {}
    warnings: list[str] = []
    if query_text:
        try:
            semantic_map = _semantic_scores(
                index, EmbeddingRuntime(cfg), query_text, len(records)
            )
        except Exception as exc:
            warnings.append(f"语义向量检索已降级：{exc}")

    keyword_query = build_query_text(request)
    ranked: list[dict[str, Any]] = []

    for idx in pool:
        record = records[idx]
        semantic_raw = semantic_map.get(idx)
        semantic_score = 0.0
        if semantic_raw is not None:
            semantic_score = max(0.0, min(1.0, (semantic_raw + 1.0) / 2.0))

        kw_score = keyword_score(keyword_query, record.get("keywords", []))
        retrieval_score = 0.55 * semantic_score + 0.45 * kw_score

        match_score, high_full, medium_full, pref_details = score_request(
            record,
            request,
            candidate_records,
        )
        star_count = stars_from_score(match_score, exact_match)
        reasons, unmet = condition_summary(record, request)
        reasons.extend(preference_summary(pref_details))

        result = {
            "product_sku": record["product_sku"],
            "factory_offer": record["factory_offer"],
            "product": record["product"],
            "packaging_options": record.get("packaging_options", []),
            "match_score": round(match_score, 2) if match_score is not None else None,
            "star_count": star_count,
            "match_reasons": reasons,
            "unmet_conditions": unmet,
        }

        if debug:
            result["_debug"] = {
                "record_id": record["record_id"],
                "keyword_score": round(kw_score, 6),
                "semantic_similarity_raw": round(semantic_raw, 6) if semantic_raw is not None else None,
                "semantic_score_normalized": round(semantic_score, 6),
                "retrieval_score": round(retrieval_score, 6),
                "high_priority_full_count": high_full,
                "medium_priority_full_count": medium_full,
                "relative_preferences": [
                    {**item, "score": round(item["score"], 6)}
                    for item in pref_details
                ],
            }

        ranked.append(
            {
                "result": result,
                "match_sort": match_score if match_score is not None else -1.0,
                "high_full": high_full,
                "medium_full": medium_full,
                "retrieval": retrieval_score,
            }
        )

    ranked.sort(
        key=lambda x: (
            x["match_sort"],
            x["high_full"],
            x["medium_full"],
            x["retrieval"],
        ),
        reverse=True,
    )

    results = [item["result"] for item in ranked[: max(1, int(top_k))]]

    return {
        "exact_match": exact_match,
        "results": results,
        "warnings": warnings,
        "index": {
            "record_count": len(records),
            "embedding_model": meta.get("embedding_model"),
            "dimension": meta.get("dimension"),
            "index_version": meta.get("index_version"),
            "status": meta.get("status"),
        },
    }
