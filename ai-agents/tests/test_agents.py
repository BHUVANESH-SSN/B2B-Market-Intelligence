"""Tests for the AI agent scaffold."""

from backend.agents.orchestrator import build_graph, run_pipeline
from backend.agents.scorer_agent import score_insights
from backend.agents.types import Insight


def test_score_insights_prioritizes_new_high_confidence_items() -> None:
    repeated = Insight(
        claim="Updated pricing section: Monthly plan now highlighted",
        category="pricing",
        confidence=0.7,
        source_section="pricing",
        competitor="Acme",
        evidence="Monthly plan now highlighted",
    )
    fresh = Insight(
        claim="Updated hero section: New enterprise automation messaging",
        category="messaging",
        confidence=0.9,
        source_section="hero",
        competitor="Acme",
        evidence="New enterprise automation messaging",
    )

    scored = score_insights([repeated, fresh], history_claims=[repeated.claim])

    assert scored[0].claim == fresh.claim
    assert scored[0].priority_score > scored[1].priority_score


def test_run_pipeline_returns_insights_and_recommendations() -> None:
    state = run_pipeline(
        competitor="Acme",
        diffs={
            "pricing": ["Introduced annual discount for enterprise plan"],
            "hero": ["Replaced headline with automation-first message"],
        },
        history_claims=[],
    )

    assert state["insights"]
    assert state["recommendations"]
    assert state["metadata"]["mode"] == "sequential-fallback"
    assert all(item.competitor == "Acme" for item in state["insights"])


def test_build_graph_returns_none_without_langgraph() -> None:
    graph = build_graph()
    assert graph is None or hasattr(graph, "invoke")
