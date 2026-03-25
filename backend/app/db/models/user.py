from __future__ import annotations

from sqlalchemy import Boolean, Index, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class User(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_clerk_user_id", "clerk_user_id", unique=True),
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    clerk_user_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    organization_links: Mapped[list["UserOrganization"]] = relationship(
        "UserOrganization",
        back_populates="user",
        cascade="all, delete-orphan",
    )
