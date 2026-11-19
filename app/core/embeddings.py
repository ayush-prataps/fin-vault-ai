"""
Embeddings Module using FastEmbed (ONNX Runtime).
Lightweight CPU inference with zero PyTorch dependency.
"""
from pathlib import Path
from typing import Optional
from fastembed import TextEmbedding

from app.utils.helpers import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
CACHE_DIR = BASE_DIR / ".fastembed_cache"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

_model: Optional[TextEmbedding] = None


def get_embedding_model() -> TextEmbedding:
    """
    Return cached TextEmbedding model or fail loudly if missing.
    Requires model files to be pre-downloaded via scripts/download_model.py.
    """
    global _model
    if _model is not None:
        return _model

    expected_model_dir = CACHE_DIR / "models--Qdrant--bge-small-en-v1.5-onnx-Q"
    if not expected_model_dir.exists():
        raise RuntimeError(
            f"Embedding model '{MODEL_NAME}' is missing from cache directory: {CACHE_DIR}. "
            "Run 'python scripts/download_model.py' to download the model before starting."
        )

    try:
        _model = TextEmbedding(
            model_name=MODEL_NAME,
            cache_dir=str(CACHE_DIR),
            local_files_only=True,
        )
        logger.info("FastEmbed model loaded successfully from %s", expected_model_dir)
        return _model
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize FastEmbed model from {CACHE_DIR}: {exc}") from exc


def embed_text(text: str) -> Optional[list[float]]:
    """
    Embed a single query string using FastEmbed.
    Matches SentenceTransformers output (384-dim, CLS pooling, L2 normalized).
    """
    if not text or not isinstance(text, str):
        return None

    model = get_embedding_model()
    embeddings = list(model.embed([text.strip()]))
    return embeddings[0].tolist() if embeddings else None


def embed_batch(texts: list[str]) -> Optional[list[list[float]]]:
    """Embed multiple texts efficiently."""
    if not texts:
        return None

    model = get_embedding_model()
    embeddings = list(model.embed([t.strip() for t in texts]))
    return [e.tolist() for e in embeddings]


class TokenizerAdapter:
    """Minimal wrapper around FastEmbed tokenizer to match encode/decode interface."""

    def __init__(self, tokenizer):
        self._tok = tokenizer

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        return self._tok.encode(text, add_special_tokens=add_special_tokens).ids

    def decode(self, token_ids: list[int], skip_special_tokens: bool = True) -> str:
        return self._tok.decode(token_ids, skip_special_tokens=skip_special_tokens)


def get_tokenizer() -> TokenizerAdapter:
    """Return wrapped tokenizer from FastEmbed model."""
    model = get_embedding_model()
    return TokenizerAdapter(model.model.tokenizer)
