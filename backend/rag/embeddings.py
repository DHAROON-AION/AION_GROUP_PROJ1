"""BGE embedding model wrapper — runs locally via sentence-transformers."""

import logging
from functools import lru_cache

from backend.core.config import get_settings

logger = logging.getLogger(__name__)

_model = None


@lru_cache
def get_embedding_model():
    """Load and cache the local BGE embedding model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        settings = get_settings()
        logger.info("Loading embedding model: %s", settings.embedding_model)
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text chunk."""
    model = get_embedding_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for multiple text chunks."""
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]


def embedding_dimension() -> int:
    """Return the dimensionality of the embedding model."""
    model = get_embedding_model()
    return model.get_sentence_embedding_dimension()
