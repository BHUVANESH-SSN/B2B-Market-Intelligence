"""Prompt templates for the market intelligence AI agents."""

from __future__ import annotations

from textwrap import dedent


ANALYST_SYSTEM_PROMPT = dedent(
    """
    You are an analyst agent for a competitor intelligence system.
    Read website diffs and extract only evidence-backed insights.

    Rules:
    - Output valid JSON only.
    - Return a JSON array, not an object.
    - Every insight must be grounded in the provided diff text.
    - Never invent product details, pricing, or positioning claims.
    - Keep claims concise and useful to a B2B product team.
    - Allowed categories: pricing, messaging, feature, positioning, other.
    - Confidence must be between 0 and 1.
    - Each array item must contain: claim, category, confidence, source_section, evidence.
    """
).strip()


RECOMMENDER_SYSTEM_PROMPT = dedent(
    """
    You are a strategy recommender for a competitor intelligence system.
    Turn scored insights into practical product or go-to-market actions.

    Rules:
    - Prioritize actions with strong evidence and clear business relevance.
    - Avoid generic advice.
    - Group similar actions when possible.
    - Output valid JSON only.
    - Return a JSON array, not an object.
    - Each array item must contain: title, rationale, priority, actions.
    """
).strip()


def build_analyst_user_prompt(competitor: str, diffs: dict[str, list[str]]) -> str:
    sections: list[str] = []
    for section, changes in diffs.items():
        rendered_changes = "\n".join(f"- {item}" for item in changes)
        sections.append(f"[{section}]\n{rendered_changes}")

    return dedent(
        f"""
        Competitor: {competitor}

        Analyze the following website changes and extract structured insights:

        {chr(10).join(sections)}
        """
    ).strip()


def build_recommender_user_prompt(competitor: str, insights_json: list[dict]) -> str:
    return dedent(
        f"""
        Competitor: {competitor}

        Create action-oriented recommendations from these scored insights:
        {insights_json}
        """
    ).strip()
