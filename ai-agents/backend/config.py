"""Environment-backed configuration for the AI agents package."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional during early setup
    load_dotenv = None


if load_dotenv is not None:
    load_dotenv()


@dataclass(slots=True)
class Settings:
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""
    analyst_model: str = "claude-3-5-sonnet-latest"
    recommender_model: str = "claude-3-5-sonnet-latest"
    llm_provider: str = "anthropic"
    environment: str = "development"
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        analyst_model=os.getenv("ANALYST_MODEL", "claude-3-5-sonnet-latest"),
        recommender_model=os.getenv("RECOMMENDER_MODEL", "claude-3-5-sonnet-latest"),
        llm_provider=os.getenv("LLM_PROVIDER", "anthropic").strip().lower(),
        environment=os.getenv("ENVIRONMENT", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
