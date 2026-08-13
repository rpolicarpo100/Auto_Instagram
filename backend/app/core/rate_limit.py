import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

_hits: dict[str, deque[float]] = defaultdict(deque)


def rate_limit(request: Request, *, limit: int = 20, window_seconds: int = 60) -> None:
    key = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = _hits[key]
    while bucket and now - bucket[0] > window_seconds:
        bucket.popleft()
    if len(bucket) >= limit:
        raise HTTPException(status_code=429, detail="RATE_LIMITED")
    bucket.append(now)
