from __future__ import annotations

from typing import Any
from uuid import UUID

from app.core.config import settings
from app.core.redis import get_json_value, get_redis_client, set_json_value


def get_job_status_key(job_id: UUID | str) -> str:
    return f"job:{job_id}"


def get_insights_cache_key(competitor_id: UUID | str) -> str:
    return f"insights:{competitor_id}"


def set_job_status(
    *,
    job_id: UUID | str,
    status: str,
    progress: int,
    step: str,
    extra: dict[str, Any] | None = None,
) -> None:
    client = get_redis_client()
    payload = {"status": status, "progress": str(progress), "step": step}
    if extra:
        payload.update({key: str(value) for key, value in extra.items() if value is not None})
    key = get_job_status_key(job_id)
    client.hset(key, mapping=payload)
    client.expire(key, settings.job_status_ttl_seconds)


def get_job_status(job_id: UUID | str) -> dict[str, str]:
    client = get_redis_client()
    return client.hgetall(get_job_status_key(job_id))


def cache_insights(competitor_id: UUID | str, payload: list[dict[str, Any]]) -> None:
    set_json_value(
        get_insights_cache_key(competitor_id),
        payload,
        ttl_seconds=settings.insights_cache_ttl_seconds,
    )


def get_cached_insights(competitor_id: UUID | str) -> list[dict[str, Any]] | None:
    payload = get_json_value(get_insights_cache_key(competitor_id))
    if payload is None:
        return None
    return list(payload)


def invalidate_insights_cache(competitor_id: UUID | str) -> None:
    client = get_redis_client()
    client.delete(get_insights_cache_key(competitor_id))
