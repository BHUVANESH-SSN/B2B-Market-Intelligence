from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.redis import get_redis_client


def build_health_response(db: Session) -> dict[str, str]:
    database_status = "ok"
    redis_status = "ok"

    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    try:
        get_redis_client().ping()
    except Exception:
        redis_status = "error"

    return {
        "status": "ok" if database_status == "ok" and redis_status == "ok" else "degraded",
        "environment": settings.environment,
        "database": database_status,
        "redis": redis_status,
    }
