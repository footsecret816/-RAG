from __future__ import annotations

import os
import tempfile
from pathlib import Path

import numpy as np

from config import RuntimeConfig
from io_utils import read_json, read_jsonl, write_json, write_jsonl
from keyword_index import build_inverted_index


RECORDS_FILE = "records.jsonl"
KEYWORDS_FILE = "keywords.json"
FAISS_FILE = "vectors.faiss"
EMBEDDINGS_FILE = "embeddings.npy"
META_FILE = "index_meta.json"


def _faiss():
    try:
        import faiss
    except ImportError as exc:
        raise RuntimeError("缺少 faiss-cpu，请先安装运行依赖") from exc
    return faiss


def paths(cfg: RuntimeConfig) -> dict[str, Path]:
    return {
        "records": cfg.records_dir / RECORDS_FILE,
        "keywords": cfg.keywords_dir / KEYWORDS_FILE,
        "faiss": cfg.vectors_dir / FAISS_FILE,
        "embeddings": cfg.vectors_dir / EMBEDDINGS_FILE,
        "meta": cfg.meta_dir / META_FILE,
    }


def build_faiss_index(embeddings: np.ndarray):
    faiss = _faiss()
    if embeddings.ndim != 2:
        raise ValueError("embeddings 必须是二维数组")
    index = faiss.IndexFlatIP(int(embeddings.shape[1]))
    if len(embeddings):
        index.add(np.asarray(embeddings, dtype=np.float32))
    return index


def _atomic_save_npy(path: Path, arr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    os.close(fd)
    try:
        with open(tmp, "wb") as f:
            np.save(f, arr)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _atomic_save_faiss(path: Path, index) -> None:
    faiss = _faiss()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    os.close(fd)
    try:
        faiss.write_index(index, tmp)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def save_index(
    cfg: RuntimeConfig,
    records: list[dict],
    embeddings: np.ndarray,
    meta: dict,
) -> None:
    if len(records) != len(embeddings):
        raise ValueError("记录数与向量数不一致")

    p = paths(cfg)
    write_jsonl(p["records"], records)
    write_json(p["keywords"], build_inverted_index(records))
    _atomic_save_npy(p["embeddings"], np.asarray(embeddings, dtype=np.float32))
    _atomic_save_faiss(p["faiss"], build_faiss_index(embeddings))
    write_json(p["meta"], meta)


def load_index(cfg: RuntimeConfig) -> tuple[list[dict], np.ndarray, object, dict]:
    p = paths(cfg)
    missing = [str(path) for path in p.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("检索索引不完整，缺少：\n" + "\n".join(missing))

    records = read_jsonl(p["records"])
    embeddings = np.load(p["embeddings"], allow_pickle=False)
    index = _faiss().read_index(str(p["faiss"]))
    meta = read_json(p["meta"])
    return records, embeddings, index, meta
