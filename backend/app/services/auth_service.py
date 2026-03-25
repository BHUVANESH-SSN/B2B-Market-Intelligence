from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.crud.organization import add_user_to_organization, create_organization, get_accessible_orgs
from app.db.crud.user import create_user, get_user_by_email
from app.db.models import User
from app.db.models.enums import OrganizationRole
from app.db.schemas.auth import AuthResponse, CurrentUserResponse, LoginRequest, SignupRequest
from app.utils.exceptions import ConflictError, ForbiddenError, UnauthorizedError


def signup_user(db: Session, payload: SignupRequest) -> AuthResponse:
    if get_user_by_email(db, payload.email) is not None:
        raise ConflictError("An account with this email already exists.")

    organization_name = payload.organization_name or f"{payload.name}'s Organization"

    try:
        user = create_user(
            db,
            name=payload.name,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
        )
        organization = create_organization(db, name=organization_name)
        add_user_to_organization(
            db,
            user_id=user.id,
            org_id=organization.id,
            role=OrganizationRole.OWNER,
        )
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return _build_auth_response(db, user)


def login_user(db: Session, payload: LoginRequest) -> AuthResponse:
    user = get_user_by_email(db, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password.")
    if not user.is_active:
        raise ForbiddenError("Your account is inactive.")
    return _build_auth_response(db, user)


def get_current_user_response(db: Session, user: User) -> CurrentUserResponse:
    memberships = get_accessible_orgs(db, user_id=user.id)
    return CurrentUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        organizations=[
            {"org_id": org_id, "org_name": org_name, "role": role}
            for org_id, org_name, role in memberships
        ],
    )


def _build_auth_response(db: Session, user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(str(user.id)),
        user=get_current_user_response(db, user),
    )
