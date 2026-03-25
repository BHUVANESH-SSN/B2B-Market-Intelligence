"""Deterministic scoring agent for prioritizing insights."""

from __future__ import annotations

from collections import Counter
from math import fsum

from backend.agents.types import Insight


def _normalize(value: float) -> float:
    return max(0.0, min(1.0, round(value, 3)))


def score_insights(insights: list[Insight], history_claims: list[str] | None = None) -> list[Insight]:
    if not insights:
        return []

    history_claims = history_claims or []
    category_counts = Counter(item.category for item in insights)

    for insight in insights:
        novelty = 1.0 if insight.claim not in history_claims else 0.35
        frequency = 0.35 + min(category_counts[insight.category] / len(insights), 0.65)
        recency = insight.confidence
        insight.novelty_score = _normalize(novelty)
        insight.frequency_score = _normalize(frequency)
        insight.recency_score = _normalize(recency)
        insight.priority_score = _normalize(
            fsum(
                [
                    insight.novelty_score * 0.4,
                    insight.frequency_score * 0.2,
                    insight.recency_score * 0.4,
                ]
            )
        )

    return sorted(insights, key=lambda item: item.priority_score, reverse=True)
