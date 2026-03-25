"""Analyst agent for turning semantic diffs into structured insights."""

from __future__ import annotations

from typing import Any, Callable, Iterable

from backend.agents.types import AgentState, Insight, InsightCategory
from backend.prompts import ANALYST_SYSTEM_PROMPT, build_analyst_user_prompt


LlmCallable = Callable[[str, str], list[dict[str, Any]]]


def _infer_category(section_name: str, change: str) -> InsightCategory:
    lower = f"{section_name} {change}".lower()
    if "price" in lower or "billing" in lower or "plan" in lower:
        return "pricing"
    if "feature" in lower or "integration" in lower or "workflow" in lower:
        return "feature"
    if "position" in lower or "category" in lower or "alternative" in lower:
        return "positioning"
    if "hero" in lower or "headline" in lower or "cta" in lower or "message" in lower:
        return "messaging"
    return "other"


def _fallback_claim(section_name: str, change: str) -> str:
    cleaned = change.strip().rstrip(".")
    prefix = f"Updated {section_name} section"
    return f"{prefix}: {cleaned}" if cleaned else prefix


def _build_fallback_insights(competitor: str, diffs: dict[str, list[str]]) -> list[Insight]:
    insights: list[Insight] = []
    for section_name, changes in diffs.items():
        for change in changes:
            insights.append(
                Insight(
                    claim=_fallback_claim(section_name, change),
                    category=_infer_category(section_name, change),
                    confidence=0.72,
                    source_section=section_name,
                    competitor=competitor,
                    evidence=change,
                )
            )
    return insights


def _normalize_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("insights", "items", "results", "data"):
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


def _coerce_llm_output(competitor: str, payload: Any) -> list[Insight]:
    normalized_items = _normalize_payload(payload)
    insights: list[Insight] = []
    for item in normalized_items:
        claim = _first_text(item, ("claim", "insight", "summary", "title", "observation"))
        if not claim:
            continue
        insights.append(
            Insight(
                claim=claim,
                category=_first_text(item, ("category", "type", "label"), "other"),
                confidence=float(item.get("confidence", item.get("score", 0.6))),
                source_section=_first_text(item, ("source_section", "section", "source"), "unknown"),
                competitor=competitor,
                evidence=_first_text(item, ("evidence", "citation", "reasoning", "source_text")),
            )
        )
    return insights


def analyze_diffs(state: AgentState, llm_client: LlmCallable | None = None) -> AgentState:
    competitor = state.get("competitor", "unknown")
    diffs = state.get("diffs", {})

    if not diffs:
        return {**state, "insights": []}

    if llm_client is None:
        insights = _build_fallback_insights(competitor, diffs)
        return {**state, "insights": insights}

    prompt = build_analyst_user_prompt(competitor, diffs)
    try:
        payload = llm_client(ANALYST_SYSTEM_PROMPT, prompt)
        insights = _coerce_llm_output(competitor, payload)
    except Exception:
        insights = []

    if not insights:
        insights = _build_fallback_insights(competitor, diffs)
    return {**state, "insights": insights}
