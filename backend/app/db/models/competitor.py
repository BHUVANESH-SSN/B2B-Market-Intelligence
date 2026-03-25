from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class Competitor(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "competitors"
    __table_args__ = (
        UniqueConstraint("org_id", "domain", name="uq_competitors_org_domain"),
        Index("idx_competitors_org", "org_id"),
    )

    org_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(Text, nullable=False)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="competitors")
    snapshots: Mapped[list["Snapshot"]] = relationship(
        "Snapshot",
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
    diffs: Mapped[list["Diff"]] = relationship(
        "Diff",
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
    insights: Mapped[list["Insight"]] = relationship(
        "Insight",
        back_populates="competitor",
        cascade="all, delete-orphan",
    )
