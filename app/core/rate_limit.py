"""
In-memory sliding-window rate limiter, global daily cap, and concurrency limiter.
Protects LLM API quota and database connections without external dependencies.
"""
import asyncio
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any
from fastapi import HTTPException, Request

from app.config import settings

RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

# Max 2 concurrent LLM queries at any given instant
CONCURRENCY_SEMAPHORE = asyncio.Semaphore(2)

_request_history: dict[str, list[float]] = defaultdict(list)
_daily_state: dict[str, Any] = {"date": "", "count": 0}
_lock = asyncio.Lock()


def get_client_ip(request: Request) -> str:
    """Extract client IP, checking X-Forwarded-For for reverse proxies like Render."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _reset_rate_limits_for_test() -> None:
    """Reset in-memory rate-limit counters (intended for unit tests)."""
    _request_history.clear()
    _daily_state["date"] = ""
    _daily_state["count"] = 0


async def check_rate_limit(request: Request) -> None:
    """Enforce per-IP sliding-window rate limit and global daily request cap."""
    ip = get_client_ip(request)
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS
    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    async with _lock:
        if _daily_state["date"] != today_utc:
            _daily_state["date"] = today_utc
            _daily_state["count"] = 0

        if _daily_state["count"] >= settings.global_daily_cap:
            raise HTTPException(
                status_code=429,
                detail="Global daily query cap reached. Please try again tomorrow.",
            )

        # Keep only timestamps within sliding window
        valid_timestamps = [ts for ts in _request_history[ip] if ts > cutoff]
        _request_history[ip] = valid_timestamps

        if len(valid_timestamps) >= RATE_LIMIT_REQUESTS:
            oldest = valid_timestamps[0]
            retry_after = max(1, int(oldest + RATE_LIMIT_WINDOW_SECONDS - now) + 1)
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

        _request_history[ip].append(now)
        _daily_state["count"] += 1
