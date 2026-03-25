"""Shared types for the AI agent pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, TypedDict


InsightCategory = Literal["pricing", "messaging", "feature", "positioning", "other"]


@dataclass(slots=True)
class Insight:
    claim: str
    category: InsightCategory
    confidence: float
    source_section: str
    competitor: str
    evidence: str
    novelty_score: float = 0.0
    frequency_score: float = 0.0
    recency_score: float = 0.0
    priority_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Recommendation:
    title: str
    rationale: str
    priority: Literal["high", "medium", "low"]
    actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentState(TypedDict, total=False):
    competitor: str
    diffs: dict[str, list[str]]
    insights: list[Insight]
    recommendations: list[Recommendation]
    history_claims: list[str]
    metadata: dict[str, Any]
