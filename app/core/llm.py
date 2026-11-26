"""
Single OpenAI-compatible LLM client driven by LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL.
Maintains temperature=0.0, timeout, max_tokens, and in-memory response/failure caching.
Supports configurable fallback (disabled in benchmark/evaluation).
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
_FAILURE_CACHE: dict[tuple[str, str, str], dict[str, Any]] = {}
_MAX_CACHE_ENTRIES = 512
_FAILURE_COOLDOWN_SECONDS = 60.0


def clear_llm_cache() -> None:
    """Clear the in-memory LLM response and failure cooldown caches."""
    with _CACHE_LOCK:
        _RESPONSE_CACHE.clear()
        _FAILURE_CACHE.clear()


def _make_cache_key(base_url: str, model: str, max_tokens: int, prompt: str) -> str:
    """Build deterministic cache key isolating base URL, model, generation params, and prompt."""
    payload = f"{base_url}|{model}|temp=0.0|max_tokens={max_tokens}|{prompt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _make_failure_key(base_url: str, model: str, api_key: str) -> tuple[str, str, str]:
    """Key failure cooldown by endpoint, model, and key fingerprint so config fixes bypass stale errors."""
    key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]
    return (base_url, model, key_hash)


def list_available_models(
    base_url: str | None = None,
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    """Query OpenAI-compatible /models endpoint."""
    target_url = (base_url or os.getenv("LLM_BASE_URL", settings.llm_base_url) or "").strip().rstrip("/")
    target_key = (api_key or os.getenv("LLM_API_KEY", settings.llm_api_key) or "").strip()
    if not target_url or not target_key:
        raise ValueError("LLM_BASE_URL and LLM_API_KEY must be configured to list models")

    resp = httpx.get(
        f"{target_url}/models",
        headers={"Authorization": f"Bearer {target_key}"},
        timeout=settings.llm_timeout_seconds,
    )
    resp.raise_for_status()
    return list(resp.json().get("data", []))


def call_llm(
    prompt: str,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    use_cache: bool = True,
    allow_fallback: bool = True,
) -> dict[str, Any]:
    """
    Call an OpenAI-compatible chat completions endpoint with temperature=0.0,
    configured timeout, and max_tokens.
    Isolates response cache keys per provider/model and caches primary failures
    briefly (cooldown TTL) so fallback does not keep retrying a dead primary endpoint.
    Fallback is disabled when allow_fallback=False (benchmark/eval) or LLM_FALLBACK_ENABLED=false.
    Raises exception on API error; never returns fake text.
    """
    target_url = (base_url or os.getenv("LLM_BASE_URL", settings.llm_base_url) or "").strip().rstrip("/")
    target_key = (api_key or os.getenv("LLM_API_KEY", settings.llm_api_key) or "").strip()
    target_model = (model or os.getenv("LLM_MODEL", settings.llm_model) or "").strip()

    if not target_url:
        raise ValueError("LLM_BASE_URL environment variable is not set")
    if not target_key:
        raise ValueError("LLM_API_KEY environment variable is not set")
    if not target_model:
        raise ValueError("LLM_MODEL environment variable is not set")

    max_tokens = settings.llm_max_tokens
    cache_key = _make_cache_key(target_url, target_model, max_tokens, prompt)

    fallback_enabled = (
        os.getenv(
            "LLM_FALLBACK_ENABLED",
            "true" if settings.llm_fallback_enabled else "false",
        )
        .strip()
        .lower()
        in ("true", "1", "yes")
    )
    fb_url = (os.getenv("LLM_FALLBACK_BASE_URL", settings.llm_fallback_base_url) or "").strip().rstrip("/")
    fb_key = (os.getenv("LLM_FALLBACK_API_KEY", settings.llm_fallback_api_key) or "").strip()
    fb_model = (os.getenv("LLM_FALLBACK_MODEL", settings.llm_fallback_model) or "").strip()
    has_fallback = (
        allow_fallback
        and fallback_enabled
        and bool(fb_url and fb_key and fb_model)
        and (fb_url, fb_model) != (target_url, target_model)
    )

    if use_cache:
        with _CACHE_LOCK:
            cached = _RESPONSE_CACHE.get(cache_key)
            if cached is not None:
                return {
                    **cached,
                    "cached": True,
                    "fallback_used": False,
                    "primary_model": None,
                    "primary_error": None,
                }

    failure_key = _make_failure_key(target_url, target_model, target_key)
    if use_cache and has_fallback:
        cached_fail_err: str | None = None
        with _CACHE_LOCK:
            fail_entry = _FAILURE_CACHE.get(failure_key)
            if fail_entry is not None:
                if time.time() - fail_entry["failed_at"] < _FAILURE_COOLDOWN_SECONDS:
                    cached_fail_err = fail_entry["error"]
                else:
                    _FAILURE_CACHE.pop(failure_key, None)

        if cached_fail_err is not None:
            logger.warning(
                "Primary model '%s' in failure cooldown (%s); routing directly to fallback '%s'.",
                target_model,
                cached_fail_err,
                fb_model,
            )
            try:
                fb_res = call_llm(
                    prompt=prompt,
                    model=fb_model,
                    base_url=fb_url,
                    api_key=fb_key,
                    use_cache=use_cache,
                    allow_fallback=False,
                )
            except Exception as fb_err:
                with _CACHE_LOCK:
                    _FAILURE_CACHE.pop(failure_key, None)
                raise RuntimeError(
                    f"Primary ({target_model}) failed: {cached_fail_err}; Fallback ({fb_model}) also failed: {fb_err}"
                ) from fb_err
            return {
                **fb_res,
                "fallback_used": True,
                "primary_model": target_model,
                "primary_error": cached_fail_err,
            }

    body: dict[str, Any] = {
        "model": target_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }
    # DeepSeek non-reasoning mode: explicitly disable thinking mode
    if "deepseek" in target_url.lower():
        body["thinking"] = {"type": "disabled"}

    start_time = time.time()
    try:
        resp = httpx.post(
            f"{target_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {target_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=settings.llm_timeout_seconds,
        )
        if resp.is_error:
            raise RuntimeError(f"LLM API HTTP {resp.status_code}: {resp.text}")

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
    except Exception as err:
        if has_fallback:
            logger.warning(
                "Primary LLM call failed (%s); switching to fallback '%s'...",
                err,
                fb_model,
            )
            if use_cache:
                with _CACHE_LOCK:
                    _FAILURE_CACHE[failure_key] = {"error": str(err), "failed_at": time.time()}
            try:
                fb_res = call_llm(
                    prompt=prompt,
                    model=fb_model,
                    base_url=fb_url,
                    api_key=fb_key,
                    use_cache=use_cache,
                    allow_fallback=False,
                )
            except Exception as fb_err:
                raise RuntimeError(
                    f"Primary ({target_model}) failed: {err}; Fallback ({fb_model}) also failed: {fb_err}"
                ) from fb_err
            return {
                **fb_res,
                "fallback_used": True,
                "primary_model": target_model,
                "primary_error": str(err),
            }
        raise

    usage = data.get("usage") or {}
    prompt_tokens = int(usage.get("prompt_tokens") or 0)
    completion_tokens = int(usage.get("completion_tokens") or 0)
    tokens_used = int(usage.get("total_tokens") or (prompt_tokens + completion_tokens))

    headers = resp.headers
    result = {
        "model": str(api_model),
        "requested_model": target_model,
        "output": content,
        "tokens_used": tokens_used,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "latency_ms": latency_ms,
        "cached": False,
        "ratelimit_remaining_tokens": headers.get("x-ratelimit-remaining-tokens"),
        "ratelimit_reset_tokens": headers.get("x-ratelimit-reset-tokens"),
        "ratelimit_remaining_requests": headers.get("x-ratelimit-remaining-requests"),
    }

    with _CACHE_LOCK:
        _FAILURE_CACHE.pop(failure_key, None)
        if use_cache:
            if len(_RESPONSE_CACHE) >= _MAX_CACHE_ENTRIES:
                _RESPONSE_CACHE.pop(next(iter(_RESPONSE_CACHE)))
            _RESPONSE_CACHE[cache_key] = result

    logger.info("LLM call completed: %s in %sms, %s tokens", api_model, latency_ms, tokens_used)
    return {
        **result,
        "fallback_used": False,
        "primary_model": None,
        "primary_error": None,
    }
