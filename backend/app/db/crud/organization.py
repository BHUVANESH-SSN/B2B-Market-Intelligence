from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Organization, UserOrganization
from app.db.models.enums import OrganizationRole


def create_organization(db: Session, *, name: str) -> Organization:
    organization = Organization(name=name)
    db.add(organization)
    db.flush()
    return organization


def add_user_to_organization(
    db: Session,
    *,
    user_id: UUID,
    org_id: UUID,
    role: OrganizationRole,
) -> UserOrganization:
    membership = UserOrganization(user_id=user_id, org_id=org_id, role=role)
    db.add(membership)
    db.flush()
    return membership


def get_accessible_org_ids(db: Session, *, user_id: UUID) -> list[UUID]:
    stmt = select(UserOrganization.org_id).where(UserOrganization.user_id == user_id)
    return list(db.scalars(stmt))


def get_accessible_orgs(db: Session, *, user_id: UUID) -> list[tuple[UUID, str, str]]:
    stmt = (
        select(Organization.id, Organization.name, UserOrganization.role)
        .join(UserOrganization, UserOrganization.org_id == Organization.id)
        .where(UserOrganization.user_id == user_id)
    )
    return [(org_id, name, role.value) for org_id, name, role in db.execute(stmt).all()]
