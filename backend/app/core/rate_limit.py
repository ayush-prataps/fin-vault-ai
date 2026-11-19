"""
In-memory sliding-window rate limiter and concurrency limiter.
Protects LLM API quota and database connections without external dependencies.
"""
import asyncio
import time
from collections import defaultdict
from fastapi import HTTPException, Request

RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

# Max 2 concurrent LLM queries at any given instant
CONCURRENCY_SEMAPHORE = asyncio.Semaphore(2)

_request_history: dict[str, list[float]] = defaultdict(list)
_lock = asyncio.Lock()


def get_client_ip(request: Request) -> str:
    """Extract client IP, checking X-Forwarded-For for reverse proxies like Render."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def check_rate_limit(request: Request) -> None:
    """Enforce sliding-window rate limit per client IP."""
    ip = get_client_ip(request)
    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS

    async with _lock:
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
