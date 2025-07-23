import time
from fastapi import Request, HTTPException
from functools import wraps
import inspect

_requests: dict[str, list[float]] = {}


def rate_limit(limit: int, window: int, key_func):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request') or args[0]
            key = key_func(request, *args, **kwargs)
            now = time.time()
            window_start = now - window
            hits = _requests.setdefault(key, [])
            hits[:] = [h for h in hits if h > window_start]
            if len(hits) >= limit:
                raise HTTPException(status_code=429, detail="rate limit exceeded")
            hits.append(now)
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
