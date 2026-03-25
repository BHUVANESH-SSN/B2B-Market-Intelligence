from __future__ import annotations

from functools import lru_cache
import json
from typing import Any

from redis import Redis

from app.core.config import settings


@lru_cache
def get_redis_client() -> Redis:
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )


def set_json_value(key: str, value: dict[str, Any] | list[Any], ttl_seconds: int | None = None) -> None:
    client = get_redis_client()
    client.set(key, json.dumps(value))
    if ttl_seconds:
        client.expire(key, ttl_seconds)


def get_json_value(key: str) -> Any | None:
    client = get_redis_client()
    payload = client.get(key)
    if payload is None:
        return None
    return json.loads(payload)
