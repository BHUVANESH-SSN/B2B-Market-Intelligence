from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import settings
from app.core.redis import get_redis_client
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    db_status = "ok"
    redis_status = "ok"

    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    finally:
        session.close()

    try:
        get_redis_client().ping()
    except Exception:
        redis_status = "error"

    overall = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    return {
        "status": overall,
        "environment": settings.environment,
        "database": db_status,
        "redis": redis_status,
    }
