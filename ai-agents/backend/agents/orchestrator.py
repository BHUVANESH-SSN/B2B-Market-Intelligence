"""Pipeline orchestration for the AI agent workflow."""

from __future__ import annotations

from typing import Any, Callable

from backend.agents.analyst_agent import analyze_diffs
from backend.agents.recommender_agent import build_recommendations
from backend.agents.scorer_agent import score_insights
from backend.agents.types import AgentState
from backend.config import get_settings
from backend.llm import get_llm_callable


LlmCallable = Callable[[str, str], list[dict[str, Any]]]


def score_node(state: AgentState) -> AgentState:
    scored = score_insights(state.get("insights", []), state.get("history_claims", []))
    return {**state, "insights": scored}


def recommend_node(state: AgentState, llm_client: LlmCallable | None = None) -> AgentState:
    recommendations = build_recommendations(
        state.get("competitor", "unknown"),
        [item.to_dict() for item in state.get("insights", [])],
        llm_client=llm_client,
    )
    return {**state, "recommendations": recommendations}


def run_pipeline(
    competitor: str,
    diffs: dict[str, list[str]],
    history_claims: list[str] | None = None,
    analyst_llm: LlmCallable | None = None,
    recommender_llm: LlmCallable | None = None,
) -> AgentState:
    settings = get_settings()
    analyst_llm = analyst_llm or get_llm_callable(settings.analyst_model)
    recommender_llm = recommender_llm or get_llm_callable(settings.recommender_model)
    mode = "model-backed" if analyst_llm or recommender_llm else "sequential-fallback"

    state: AgentState = {
        "competitor": competitor,
        "diffs": diffs,
        "history_claims": history_claims or [],
        "metadata": {"mode": mode, "provider": settings.llm_provider},
    }
    state = analyze_diffs(state, llm_client=analyst_llm)
    state = score_node(state)
    state = recommend_node(state, llm_client=recommender_llm)
    return state


def build_graph() -> Any:
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError:
        return None

    graph = StateGraph(AgentState)
    graph.add_node("analyze", analyze_diffs)
    graph.add_node("score", score_node)
    graph.add_node("recommend", recommend_node)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "score")
    graph.add_edge("score", "recommend")
    graph.add_edge("recommend", END)
    return graph.compile()
