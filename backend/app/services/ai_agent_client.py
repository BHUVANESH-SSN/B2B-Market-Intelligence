from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class AIAgentIntegrationError(RuntimeError):
    """Raised when the AI agent service is unavailable or misconfigured."""


def request_agent_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    if not settings.ai_agent_enabled:
        raise AIAgentIntegrationError("AI agent integration is disabled.")
    if not settings.ai_agent_base_url:
        raise AIAgentIntegrationError("AI agent base URL is not configured.")

    url = f"{settings.ai_agent_base_url.rstrip('/')}{settings.ai_agent_analyze_path}"

    try:
        with httpx.Client(timeout=settings.ai_agent_timeout_seconds) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise AIAgentIntegrationError(f"AI agent request failed: {exc}") from exc

    data = response.json()
    if not isinstance(data, dict):
        raise AIAgentIntegrationError("AI agent response must be a JSON object.")

    return data
