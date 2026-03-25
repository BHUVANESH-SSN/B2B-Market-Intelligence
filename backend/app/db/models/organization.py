from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.competitor import Competitor
    from app.db.models.job import Job
    from app.db.models.membership import Membership
    from app.db.models.report import Report


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    memberships: Mapped[list["Membership"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    competitors: Mapped[list["Competitor"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    jobs: Mapped[list["Job"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
