from __future__ import annotations

from app.db.schemas.common import TimestampedModel


class UserRead(TimestampedModel):
    clerk_user_id: str | None
    name: str
    email: str
    is_active: bool
