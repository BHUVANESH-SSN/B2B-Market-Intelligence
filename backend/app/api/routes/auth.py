from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, get_auth_context, get_db
from app.db.schemas.auth import CurrentUserResponse
from app.services.auth_service import get_current_user_response

router = APIRouter()


@router.get("/me", response_model=CurrentUserResponse)
def me(
    db: Session = Depends(get_db),
    auth_context: AuthContext = Depends(get_auth_context),
) -> CurrentUserResponse:
    return get_current_user_response(db, auth_context.user, auth_context.claims)
