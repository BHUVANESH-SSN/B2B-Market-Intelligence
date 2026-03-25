from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.db.schemas.analysis import AnalysisRunRequest, AnalysisRunResponse
from app.services.analysis_service import queue_analysis_job

router = APIRouter()


@router.post("/run", response_model=AnalysisRunResponse, status_code=status.HTTP_202_ACCEPTED)
def run_analysis(
    payload: AnalysisRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalysisRunResponse:
    return queue_analysis_job(db, user=current_user, payload=payload)
