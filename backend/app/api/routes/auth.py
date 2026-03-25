from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import AuthContext, get_auth_context
from app.db.schemas.auth import CurrentUserResponse
from app.services.auth_service import build_current_user_response


router = APIRouter()


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(auth: AuthContext = Depends(get_auth_context)) -> CurrentUserResponse:
    return build_current_user_response(auth)
