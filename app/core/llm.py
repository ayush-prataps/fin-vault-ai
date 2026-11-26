"""
Dual-provider LLM client supporting DeepSeek and Groq side-by-side with
prefix routing, automatic failover, and OpenAI-compatible completions.
Maintains temperature=0.0, timeout, max_tokens, and in-memory response caching
keyed by provider, base URL, model, and prompt hash.
Never returns fake answers on error.
"""
import hashlib
import os
import threading
import time
from typing import Any

import httpx

from app.config import settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)

_CACHE_LOCK = threading.Lock()
_RESPONSE_CACHE: dict[str, dict[str, Any]] = {}
_MAX_CACHE_ENTRIES = 512


def resolve_provider(
    model: str | None = None,
    provider: str | None = None,
) -> tuple[str, str, str, str]:
    """
    Resolve (provider_name, base_url, api_key, model_name).
    Supports explicit provider, prefix routing ('deepseek/...', 'groq/...'),
    known model heuristics, and environment-level fallbacks.
    """
    # 1. Explicit provider parameter
    req_prov = (provider or "").strip().lower()
    clean_model = (model or "").strip()

    # Strip prefixes if provided as "deepseek/foo" or "groq/foo"
    if clean_model.startswith("deepseek/"):
        req_prov = "deepseek"
        clean_model = clean_model.split("/", 1)[1]
    elif clean_model.startswith("groq/"):
        req_prov = "groq"
        clean_model = clean_model.split("/", 1)[1]
        if clean_model.startswith("qwen3") or clean_model.startswith("qwen."):
            clean_model = f"qwen/{clean_model}"

    # Heuristic detection from model name if provider not explicitly set
    if not req_prov and clean_model:
        low_model = clean_model.lower()
        if "deepseek" in low_model:
            req_prov = "deepseek"
        elif any(k in low_model for k in ("qwen", "llama", "gemma", "mixtral", "gpt-oss")):
            req_prov = "groq"

    # Route according to identified provider
    if req_prov == "deepseek":
        base_url = (os.getenv("DEEPSEEK_BASE_URL", settings.deepseek_base_url) or "https://api.deepseek.com").strip().rstrip("/")
        api_key = (os.getenv("DEEPSEEK_API_KEY", settings.deepseek_api_key) or os.getenv("LLM_API_KEY", settings.llm_api_key) or "").strip()
        target_model = clean_model or os.getenv("DEEPSEEK_MODEL", settings.deepseek_model) or "deepseek-flash"
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY (or LLM_API_KEY) environment variable is not set")
        return "deepseek", base_url, api_key, target_model

    if req_prov == "groq":
        base_url = (os.getenv("GROQ_BASE_URL", settings.groq_base_url) or "https://api.groq.com/openai/v1").strip().rstrip("/")
        api_key = (os.getenv("GROQ_API_KEY", settings.groq_api_key) or "").strip()
        target_model = clean_model or os.getenv("GROQ_MODEL", settings.groq_model) or "qwen/qwen3.8-27b"
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return "groq", base_url, api_key, target_model

    # Generic / Default fallback
    base_url = (os.getenv("LLM_BASE_URL", settings.llm_base_url) or "").strip().rstrip("/")
    api_key = (os.getenv("LLM_API_KEY", settings.llm_api_key) or "").strip()
    target_model = clean_model or os.getenv("LLM_MODEL", settings.llm_model) or ""

    if base_url and api_key:
        prov = "deepseek" if "deepseek" in base_url.lower() else ("groq" if "groq" in base_url.lower() else "custom")
        return prov, base_url, api_key, target_model or ("deepseek-flash" if prov == "deepseek" else "qwen/qwen3.8-27b")

    # If generic variables empty, check provider-specific keys
    ds_key = (os.getenv("DEEPSEEK_API_KEY", settings.deepseek_api_key) or "").strip()
    if ds_key:
        return "deepseek", settings.deepseek_base_url, ds_key, target_model or settings.deepseek_model

    groq_key = (os.getenv("GROQ_API_KEY", settings.groq_api_key) or "").strip()
    if groq_key:
        return "groq", settings.groq_base_url, groq_key, target_model or settings.groq_model

    raise ValueError("LLM provider credentials are not configured (set LLM_API_KEY, DEEPSEEK_API_KEY, or GROQ_API_KEY)")


def get_fallback_provider(current_provider: str) -> tuple[str, str, str, str] | None:
    """Return fallback provider (prov, base_url, api_key, model) if configured and enabled."""
    if not settings.llm_fallback_enabled:
        return None

    if current_provider == "deepseek":
        groq_key = (os.getenv("GROQ_API_KEY", settings.groq_api_key) or "").strip()
        if groq_key:
            return "groq", settings.groq_base_url, groq_key, settings.groq_model

    if current_provider == "groq":
        ds_key = (os.getenv("DEEPSEEK_API_KEY", settings.deepseek_api_key) or os.getenv("LLM_API_KEY", settings.llm_api_key) or "").strip()
        if ds_key:
            return "deepseek", settings.deepseek_base_url, ds_key, settings.deepseek_model

    return None


def clear_llm_cache() -> None:
    """Clear the in-memory LLM response cache."""
    with _CACHE_LOCK:
        _RESPONSE_CACHE.clear()


def _make_cache_key(provider: str, base_url: str, model: str, max_tokens: int, prompt: str) -> str:
    """Build deterministic cache key isolating provider, model, generation params, and prompt."""
    payload = f"{provider}|{base_url}|{model}|temp=0.0|max_tokens={max_tokens}|{prompt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def list_available_models(provider: str | None = None) -> list[dict[str, Any]]:
    """Query OpenAI-compatible /models endpoint for DeepSeek, Groq, or both."""
    results: list[dict[str, Any]] = []

    if provider in ("all", None):
        targets = []
        try:
            p, u, k, _ = resolve_provider(provider="deepseek")
            targets.append((p, u, k))
        except Exception:
            pass
        try:
            p, u, k, _ = resolve_provider(provider="groq")
            targets.append((p, u, k))
        except Exception:
            pass
        if not targets:
            p, u, k, _ = resolve_provider()
            targets.append((p, u, k))
    else:
        p, u, k, _ = resolve_provider(provider=provider)
        targets = [(p, u, k)]

    for prov, base_url, api_key in targets:
        try:
            resp = httpx.get(
                f"{base_url}/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=settings.llm_timeout_seconds,
            )
            resp.raise_for_status()
            for m in resp.json().get("data", []):
                m_copy = dict(m)
                m_copy["provider"] = prov
                results.append(m_copy)
        except Exception as e:
            logger.warning("Failed to list models from %s (%s): %s", prov, base_url, e)

    return results


def call_llm(
    prompt: str,
    model: str | None = None,
    provider: str | None = None,
    use_cache: bool = True,
    allow_fallback: bool = True,
) -> dict[str, Any]:
    """
    Call an OpenAI-compatible chat completions endpoint with temperature=0.0,
    configured timeout, and max_tokens.
    Supports provider routing and automatic failover between DeepSeek and Groq.
    Records the model name returned by the API response and real token usage.
    Raises exception on API error; never returns fake text.
    """
    prov, base_url, api_key, target_model = resolve_provider(model=model, provider=provider)
    if not target_model:
        raise ValueError(f"LLM model is not configured for provider '{prov}'")

    max_tokens = settings.llm_max_tokens
    cache_key = _make_cache_key(prov, base_url, target_model, max_tokens, prompt)

    if use_cache:
        with _CACHE_LOCK:
            cached = _RESPONSE_CACHE.get(cache_key)
            if cached is not None:
                return {**cached, "cached": True}

    body: dict[str, Any] = {
        "model": target_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }
    # DeepSeek enables thinking by default unless explicitly disabled
    if prov == "deepseek" or "deepseek" in base_url.lower():
        body["thinking"] = {"type": "disabled"}

    start_time = time.time()
    resp = None
    try:
        resp = httpx.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=settings.llm_timeout_seconds,
        )
        if resp.is_error:
            raise RuntimeError(f"LLM API HTTP {resp.status_code}: {resp.text}")
    except Exception as err:
        # Check if fallback is available and allowed
        fallback_cfg = get_fallback_provider(prov) if allow_fallback else None
        if fallback_cfg:
            fb_prov, fb_url, fb_key, fb_model = fallback_cfg
            logger.warning(
                "Primary provider '%s' failed (%s). Triggering fallback to '%s' (%s)...",
                prov,
                err,
                fb_prov,
                fb_model,
            )
            fb_result = call_llm(
                prompt=prompt,
                model=fb_model,
                provider=fb_prov,
                use_cache=use_cache,
                allow_fallback=False,
            )
            fb_result["fallback_from"] = prov
            return fb_result
        # If no fallback or fallback disabled, re-raise error
        raise

    data = resp.json()
    latency_ms = int((time.time() - start_time) * 1000)

    api_model = data.get("model")
    if not api_model:
        raise RuntimeError("LLM API response missing required 'model' field")

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("LLM API response returned empty 'choices'")
    content = (choices[0].get("message") or {}).get("content")
    if content is None:
        raise RuntimeError("LLM API response missing message content")

    usage = data.get("usage") or {}
    prompt_tokens = int(usage.get("prompt_tokens") or 0)
    completion_tokens = int(usage.get("completion_tokens") or 0)
    tokens_used = int(usage.get("total_tokens") or (prompt_tokens + completion_tokens))

    headers = resp.headers
    result = {
        "model": str(api_model),
        "requested_model": target_model,
        "provider": prov,
        "output": content,
        "tokens_used": tokens_used,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "latency_ms": latency_ms,
        "cached": False,
        "fallback_from": None,
        "ratelimit_remaining_tokens": headers.get("x-ratelimit-remaining-tokens"),
        "ratelimit_reset_tokens": headers.get("x-ratelimit-reset-tokens"),
        "ratelimit_remaining_requests": headers.get("x-ratelimit-remaining-requests"),
    }

    if use_cache:
        with _CACHE_LOCK:
            if len(_RESPONSE_CACHE) >= _MAX_CACHE_ENTRIES:
                _RESPONSE_CACHE.pop(next(iter(_RESPONSE_CACHE)))
            _RESPONSE_CACHE[cache_key] = result

    logger.info("LLM call completed: %s (%s) in %sms, %s tokens", api_model, prov, latency_ms, tokens_used)
    return result
