from __future__ import annotations

import re
from collections import defaultdict
from typing import Iterable


_SPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    return _SPACE_RE.sub(" ", (text or "").casefold().strip())


def build_inverted_index(records: list[dict]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = defaultdict(list)
    for record in records:
        rid = record["record_id"]
        for keyword in record.get("keywords", []):
            key = normalize_text(str(keyword))
            if key:
                index[key].append(rid)
    return dict(index)


def build_query_text(request: dict) -> str:
    parts: list[str] = []
    semantic = request.get("semantic_query")
    if semantic:
        parts.append(str(semantic))

    for group in ("hard_conditions", "soft_conditions"):
        for condition in request.get(group, []) or []:
            value = condition.get("value")
            if isinstance(value, list):
                parts.extend(str(v) for v in value)
            elif value is not None:
                parts.append(str(value))

    return normalize_text(" ".join(parts))


def keyword_score(query_text: str, keywords: Iterable[str]) -> float:
    query = normalize_text(query_text)
    if not query:
        return 0.0

    keys = [normalize_text(str(k)) for k in keywords if normalize_text(str(k))]
    if not keys:
        return 0.0

    matched = sum(1 for k in keys if k in query)
    if matched == 0:
        return 0.0

    denominator = min(max(len(keys), 1), 8)
    return min(1.0, matched / denominator)
