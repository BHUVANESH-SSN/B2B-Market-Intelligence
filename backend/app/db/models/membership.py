from __future__ import annotations

from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.enums import OrganizationRole
from app.db.session import Base


class UserOrganization(Base):
    __tablename__ = "user_organizations"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    org_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role: Mapped[OrganizationRole] = mapped_column(
        Enum(OrganizationRole, name="organization_role", native_enum=False),
        nullable=False,
        default=OrganizationRole.MEMBER,
        server_default=OrganizationRole.MEMBER.value,
    )

    user: Mapped["User"] = relationship("User", back_populates="organization_links")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="user_links")
