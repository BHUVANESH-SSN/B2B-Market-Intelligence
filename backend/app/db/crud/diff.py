from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.db.models.diff import Diff


def create_diff(
    db: Session,
    *,
    competitor_id,
    old_snapshot_id,
    new_snapshot_id,
    diff_payload: dict[str, list[str]],
) -> Diff:
    diff = Diff(
        competitor_id=competitor_id,
        old_snapshot_id=old_snapshot_id,
        new_snapshot_id=new_snapshot_id,
        diff_text=json.dumps(diff_payload, indent=2),
        diff_payload=diff_payload,
    )
    db.add(diff)
    db.flush()
    return diff
