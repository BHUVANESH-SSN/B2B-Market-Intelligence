from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.diff import Diff
    from app.db.models.insight import Insight
    from app.db.models.organization import Organization
    from app.db.models.report import Report
    from app.db.models.snapshot import Snapshot


class Competitor(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "competitors"
    __table_args__ = (
        UniqueConstraint("org_id", "domain", name="uq_competitors_org_domain"),
        Index("idx_competitors_org", "org_id"),
    )

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="competitors")
    snapshots: Mapped[list["Snapshot"]] = relationship(
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
    diffs: Mapped[list["Diff"]] = relationship(
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
    insights: Mapped[list["Insight"]] = relationship(
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
    reports: Mapped[list["Report"]] = relationship(
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
