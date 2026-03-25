"""Input and output helpers for the local AI pipeline contract."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PipelineInput:
    competitor: str
    diffs: dict[str, list[str]] = field(default_factory=dict)
    history_claims: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipelineInput":
        competitor = str(data.get("competitor", "")).strip()
        if not competitor:
            raise ValueError("Input must include a non-empty 'competitor'")

        raw_diffs = data.get("diffs", {})
        if not isinstance(raw_diffs, dict):
            raise ValueError("'diffs' must be an object mapping section names to lists of strings")

        diffs: dict[str, list[str]] = {}
        for section, changes in raw_diffs.items():
            if not isinstance(changes, list):
                raise ValueError(f"'diffs.{section}' must be a list of strings")
            diffs[str(section)] = [str(item).strip() for item in changes if str(item).strip()]

        raw_history = data.get("history_claims", [])
        if not isinstance(raw_history, list):
            raise ValueError("'history_claims' must be a list of strings")

        history_claims = [str(item).strip() for item in raw_history if str(item).strip()]
        return cls(competitor=competitor, diffs=diffs, history_claims=history_claims)

    @classmethod
    def from_json(cls, raw: str) -> "PipelineInput":
        return cls.from_dict(json.loads(raw))


@dataclass(slots=True)
class PipelineOutput:
    metadata: dict[str, Any]
    insights: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "insights": self.insights,
            "recommendations": self.recommendations,
        }
