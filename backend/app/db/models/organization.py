from __future__ import annotations

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class Organization(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(Text, nullable=False)

    user_links: Mapped[list["UserOrganization"]] = relationship(
        "UserOrganization",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    competitors: Mapped[list["Competitor"]] = relationship(
        "Competitor",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    reports: Mapped[list["Report"]] = relationship(
        "Report",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    jobs: Mapped[list["Job"]] = relationship(
        "Job",
        back_populates="organization",
        passive_deletes=True,
    )
