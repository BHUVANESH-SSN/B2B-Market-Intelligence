from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.competitor import Competitor
    from app.db.models.diff import Diff


class Snapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "snapshots"
    __table_args__ = (Index("idx_snapshots_competitor", "competitor_id"),)

    competitor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    storage_path: Mapped[str | None] = mapped_column(Text, nullable=True)

    competitor: Mapped["Competitor"] = relationship(back_populates="snapshots")
    old_diffs: Mapped[list["Diff"]] = relationship(
        back_populates="old_snapshot",
        foreign_keys="Diff.old_snapshot_id",
    )
    new_diffs: Mapped[list["Diff"]] = relationship(
        back_populates="new_snapshot",
        foreign_keys="Diff.new_snapshot_id",
    )
