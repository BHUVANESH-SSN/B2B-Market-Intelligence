from __future__ import annotations

from app.api.deps import AuthContext
from app.db.schemas.auth import CurrentUserResponse, OrganizationMembershipRead


def build_current_user_response(auth: AuthContext) -> CurrentUserResponse:
    organizations = [
        OrganizationMembershipRead(
            id=membership.organization.id,
            name=membership.organization.name,
            role=membership.role.value if hasattr(membership.role, "value") else str(membership.role),
        )
        for membership in auth.user.memberships
    ]
    return CurrentUserResponse(
        id=auth.user.id,
        created_at=auth.user.created_at,
        clerk_user_id=auth.user.clerk_user_id,
        name=auth.user.name,
        email=auth.user.email,
        is_active=auth.user.is_active,
        organizations=organizations,
        session_id=auth.principal.session_id,
        token_claims=auth.principal.claims,
    )
