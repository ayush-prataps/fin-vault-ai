import time
from typing import Any
from groq import Groq

from app.config import settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)


def get_client() -> Groq:
    """Return an authenticated Groq client or raise an error."""
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return Groq(api_key=settings.groq_api_key)


def list_available_groq_models() -> list[str]:
    """Query Groq API for available models."""
    client = get_client()
    models = client.models.list()
    return [m.id for m in models.data]


def call_llm(prompt: str, model: str | None = None) -> dict[str, Any]:
    """
    Call Groq LLM with temperature 0.
    Tracks real token usage and latency.
    Raises exception on error; never returns mock answers.
    """
    target_model = model or settings.groq_model
    if not target_model:
        raise ValueError("GROQ_MODEL is not configured")

    client = get_client()
    start_time = time.time()

    response = client.chat.completions.create(
        model=target_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    latency_ms = int((time.time() - start_time) * 1000)
    content = response.choices[0].message.content if response.choices else ""

    tokens_used = 0
    if hasattr(response, "usage") and response.usage:
        tokens_used = response.usage.total_tokens or 0

    logger.info("LLM call completed: %s in %sms, %s tokens", target_model, latency_ms, tokens_used)

    return {
        "model": target_model,
        "output": content,
        "tokens_used": tokens_used,
        "latency_ms": latency_ms,
    }
