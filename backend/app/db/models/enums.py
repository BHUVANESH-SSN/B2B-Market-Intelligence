from __future__ import annotations

from enum import StrEnum


class MembershipRole(StrEnum):
    OWNER = "owner"
    MEMBER = "member"


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
