"""Recommendation agent for turning insights into actions."""

from __future__ import annotations

from typing import Any, Callable

from backend.agents.types import Recommendation
from backend.prompts import RECOMMENDER_SYSTEM_PROMPT, build_recommender_user_prompt


LlmCallable = Callable[[str, str], list[dict[str, Any]]]


def _priority_for_score(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.6:
        return "medium"
    return "low"


def _normalize_priority(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"high", "medium", "low"}:
        return normalized
    return "medium"


def _fallback_recommendations(insights_json: list[dict[str, Any]]) -> list[Recommendation]:
    recommendations: list[Recommendation] = []
    for item in insights_json[:3]:
        recommendations.append(
            Recommendation(
                title=f"Respond to {item['category']} change",
                rationale=item["claim"],
                priority=_priority_for_score(float(item.get("priority_score", 0.0))),
                actions=[
                    f"Review impact of the competitor's {item['category']} update.",
                    f"Validate whether our roadmap should answer: {item['claim']}",
                ],
            )
        )
    return recommendations


def _normalize_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("recommendations", "items", "results", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _first_text(item: dict[str, Any], keys: tuple[str, ...], default: str = "") -> str:
    for key in keys:
        value = item.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def build_recommendations(
    competitor: str,
    insights_json: list[dict[str, Any]],
    llm_client: LlmCallable | None = None,
) -> list[Recommendation]:
    if not insights_json:
        return []

    if llm_client is None:
        return _fallback_recommendations(insights_json)

    prompt = build_recommender_user_prompt(competitor, insights_json)
    try:
        payload = llm_client(RECOMMENDER_SYSTEM_PROMPT, prompt)
        normalized_items = _normalize_payload(payload)
        recommendations = [
            Recommendation(
                title=_first_text(item, ("title", "recommendation", "action"), "Recommendation"),
                rationale=_first_text(item, ("rationale", "reason", "why"), "Derived from competitor changes."),
                priority=_normalize_priority(_first_text(item, ("priority",), "medium")),
                actions=[str(action).strip() for action in item.get("actions", []) if str(action).strip()],
            )
            for item in normalized_items
        ]
        recommendations = [item for item in recommendations if item.title]
    except Exception:
        recommendations = []

    if not recommendations:
        return _fallback_recommendations(insights_json)
    return recommendations
