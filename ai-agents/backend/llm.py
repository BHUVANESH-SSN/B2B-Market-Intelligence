"""Helpers for creating model-backed callables for agent nodes."""

from __future__ import annotations

import json
from typing import Any, Callable

from backend.config import get_settings


LlmCallable = Callable[[str, str], list[dict[str, Any]]]


def _extract_json_array(text: str) -> list[dict[str, Any]]:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("Model response did not contain a JSON array")
    payload = json.loads(text[start : end + 1])
    if not isinstance(payload, list):
        raise ValueError("Model response JSON was not a list")
    return payload


def _anthropic_callable(model: str) -> LlmCallable | None:
    settings = get_settings()
    if not settings.anthropic_api_key:
        return None

    try:
        from anthropic import Anthropic
    except ImportError:
        return None

    client = Anthropic(api_key=settings.anthropic_api_key)

    def call(system_prompt: str, user_prompt: str) -> list[dict[str, Any]]:
        response = client.messages.create(
            model=model,
            max_tokens=1200,
            temperature=0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = "".join(
            block.text for block in response.content if getattr(block, "type", "") == "text"
        )
        return _extract_json_array(text)

    return call


def _openai_callable(model: str) -> LlmCallable | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)

    def call(system_prompt: str, user_prompt: str) -> list[dict[str, Any]]:
        response = client.responses.create(
            model=model,
            temperature=0,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = getattr(response, "output_text", "")
        return _extract_json_array(text)

    return call


def _groq_callable(model: str) -> LlmCallable | None:
    settings = get_settings()
    if not settings.groq_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(
        api_key=settings.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    def call(system_prompt: str, user_prompt: str) -> list[dict[str, Any]]:
        response = client.responses.create(
            model=model,
            temperature=0,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = getattr(response, "output_text", "")
        return _extract_json_array(text)

    return call


def get_llm_callable(model: str) -> LlmCallable | None:
    settings = get_settings()
    provider = settings.llm_provider

    if provider == "groq":
        return _groq_callable(model)
    if provider == "openai":
        return _openai_callable(model)
    if provider == "anthropic":
        return _anthropic_callable(model)
    return None
