from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.health_service import build_health_response


router = APIRouter()


@router.get("/health")
async def health(db: Session = Depends(get_db)) -> dict[str, str]:
    return build_health_response(db)
