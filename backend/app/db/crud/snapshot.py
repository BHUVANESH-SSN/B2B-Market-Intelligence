from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.snapshot import Snapshot


def create_snapshot(
    db: Session,
    *,
    competitor_id,
    content: str,
    content_hash: str,
    storage_path: str | None,
) -> Snapshot:
    snapshot = Snapshot(
        competitor_id=competitor_id,
        content=content,
        content_hash=content_hash,
        storage_path=storage_path,
    )
    db.add(snapshot)
    db.flush()
    return snapshot


def get_latest_snapshot(db: Session, *, competitor_id) -> Snapshot | None:
    return db.scalar(
        select(Snapshot)
        .where(Snapshot.competitor_id == competitor_id)
        .order_by(Snapshot.created_at.desc())
        .limit(1)
    )
