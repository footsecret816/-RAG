from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from config import (
    MODEL_DIMENSION,
    MODEL_ID,
    PRODUCT_PREFIX,
    QUERY_PREFIX,
    RuntimeConfig,
)


@dataclass
class EmbeddingRuntime:
    config: RuntimeConfig

    def __post_init__(self) -> None:
        self._model = None

    def _load(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "缺少 sentence-transformers。请先安装 04-search/runtime/requirements.txt"
            ) from exc

        kwargs = {
            "cache_folder": str(self.config.model_cache_dir),
            "device": "cpu",
        }
        if self.config.model_revision:
            kwargs["revision"] = self.config.model_revision

        self._model = SentenceTransformer(self.config.model_source, **kwargs)

        dim = self._model.get_sentence_embedding_dimension()
        if dim != MODEL_DIMENSION:
            raise RuntimeError(
                f"向量维度不符合 V1 规范：期望 {MODEL_DIMENSION}，实际 {dim}"
            )
        return self._model

    def encode_products(self, semantic_bodies: list[str]) -> np.ndarray:
        texts = [PRODUCT_PREFIX + text for text in semantic_bodies]
        return self._encode(texts)

    def encode_queries(self, queries: list[str]) -> np.ndarray:
        texts = [QUERY_PREFIX + text for text in queries]
        return self._encode(texts)

    def _encode(self, texts: list[str]) -> np.ndarray:
        model = self._load()
        vectors = model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        vectors = np.asarray(vectors, dtype=np.float32)
        if vectors.ndim != 2 or vectors.shape[1] != MODEL_DIMENSION:
            raise RuntimeError(f"Embedding 输出形状异常：{vectors.shape}")
        if not np.isfinite(vectors).all():
            raise RuntimeError("Embedding 输出包含 NaN 或 Infinity")
        return vectors

    @property
    def model_id(self) -> str:
        return MODEL_ID
