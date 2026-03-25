from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.mixins import CreatedAtMixin, UUIDPrimaryKeyMixin
from app.db.session import Base


class Snapshot(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "snapshots"
    __table_args__ = (Index("idx_snapshots_competitor", "competitor_id"),)

    competitor_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(Text, nullable=False)
    storage_path: Mapped[str | None] = mapped_column(Text, nullable=True)

    competitor: Mapped["Competitor"] = relationship("Competitor", back_populates="snapshots")
    old_diffs: Mapped[list["Diff"]] = relationship(
        "Diff",
        back_populates="old_snapshot",
        foreign_keys="Diff.old_snapshot_id",
    )
    new_diffs: Mapped[list["Diff"]] = relationship(
        "Diff",
        back_populates="new_snapshot",
        foreign_keys="Diff.new_snapshot_id",
    )
