from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class Diff(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "diffs"
    __table_args__ = (Index("idx_diffs_competitor", "competitor_id"),)

    competitor_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    old_snapshot_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("snapshots.id", ondelete="SET NULL"),
        nullable=True,
    )
    new_snapshot_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("snapshots.id", ondelete="SET NULL"),
        nullable=True,
    )
    diff_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    competitor: Mapped["Competitor"] = relationship("Competitor", back_populates="diffs")
    old_snapshot: Mapped["Snapshot"] = relationship(
        "Snapshot",
        back_populates="old_diffs",
        foreign_keys=[old_snapshot_id],
    )
    new_snapshot: Mapped["Snapshot"] = relationship(
        "Snapshot",
        back_populates="new_diffs",
        foreign_keys=[new_snapshot_id],
    )
    insights: Mapped[list["Insight"]] = relationship(
        "Insight",
        back_populates="diff",
        cascade="all, delete-orphan",
    )
