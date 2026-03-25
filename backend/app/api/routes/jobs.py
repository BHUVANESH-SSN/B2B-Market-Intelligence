from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.schemas.job import JobRead
from app.db.session import get_db
from app.services.analysis_service import get_job_for_user


router = APIRouter()


@router.get("/{job_id}", response_model=JobRead)
async def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JobRead:
    return get_job_for_user(db, user=user, job_id=job_id)
