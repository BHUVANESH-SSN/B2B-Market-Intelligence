from __future__ import annotations

import json
from typing import Any

from app.core.redis import get_redis_client


def set_job_status(job_id: str, *, status: str, progress: int, step: str, extra: dict[str, Any] | None = None) -> None:
    payload = {"status": status, "progress": progress, "step": step, **(extra or {})}
    client = get_redis_client()
    client.hset(
        f"job:{job_id}",
        mapping={
            key: json.dumps(value) if isinstance(value, (dict, list)) else value
            for key, value in payload.items()
        },
    )


def get_job_status(job_id: str) -> dict[str, Any]:
    client = get_redis_client()
    data = client.hgetall(f"job:{job_id}")
    parsed: dict[str, Any] = {}
    for key, value in data.items():
        try:
            parsed[key] = json.loads(value)
        except Exception:
            parsed[key] = value
    return parsed


def cache_competitor_insights(competitor_id: str, insights: list[dict[str, Any]]) -> None:
    get_redis_client().set(f"insights:{competitor_id}", json.dumps(insights), ex=3600)


def get_cached_competitor_insights(competitor_id: str) -> list[dict[str, Any]] | None:
    raw = get_redis_client().get(f"insights:{competitor_id}")
    if not raw:
        return None
    return json.loads(raw)
