import json
import hashlib
from typing import Callable, TypeVar, Dict, Any
import redis
from .config import settings

_r = redis.from_url(settings.redis_url, decode_responses=True) # pyright: ignore[reportUnknownMemberType]

def _key(ns: str, target: str) -> str:
    h = hashlib.sha256(target.encode()).hexdigest()[:16]
    return f"nta:{ns}:{h}"

T = TypeVar("T", bound=Dict[str, Any])

def cached(ns: str, ttl: int) -> Callable[[Callable[[str], T]], Callable[[str], T]]:
    def wrap(fn: Callable[[str], T]) -> Callable[[str], T]:
        def inner(target: str) -> T:
            # generate cache key
            k = _key(ns, target)

            # try reading from Redis
            val = _r.get(k) # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            if val is not None:
                try:
                    return json.loads(val) | {"cache": True} # pyright: ignore[reportArgumentType]
                except Exception:
                    pass  # fallback if corrupted

            # if no cache, compute result
            res = fn(target)

            # try storing in Redis
            try:
                _r.setex(k, ttl, json.dumps(res)) # pyright: ignore[reportUnknownMemberType]
            except Exception:
                pass

            return res
        return inner
    return wrap
