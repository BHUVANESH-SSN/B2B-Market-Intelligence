from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.schemas.analysis import AnalysisRunRequest, AnalysisRunResponse
from app.db.session import get_db
from app.services.analysis_service import enqueue_analysis


router = APIRouter()


@router.post("/run", response_model=AnalysisRunResponse, status_code=status.HTTP_202_ACCEPTED)
async def run_analysis(
    payload: AnalysisRunRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AnalysisRunResponse:
    job = enqueue_analysis(db, user=user, payload=payload)
    return AnalysisRunResponse(job_id=job.id, status=job.status)
