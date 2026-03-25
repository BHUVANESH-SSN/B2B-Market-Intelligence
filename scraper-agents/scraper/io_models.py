"""Input and output helpers for scraper agents."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DiffPayload:
    competitor: str
    diffs: dict[str, list[str]]
    history_claims: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "competitor": self.competitor,
            "diffs": self.diffs,
            "history_claims": self.history_claims,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
