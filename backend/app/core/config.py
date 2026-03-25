from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    app_name: str = "Market Intelligence API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    database_url: str = Field(..., alias="DATABASE_URL")
    redis_url: str = Field(..., alias="REDIS_URL")
    secret_key: str = Field("change-me", alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")

    clerk_issuer: str = Field("", alias="CLERK_ISSUER")
    clerk_jwks_url: str = Field("", alias="CLERK_JWKS_URL")
    clerk_secret_key: str = Field("", alias="CLERK_SECRET_KEY")
    clerk_authorized_parties: str = Field("", alias="CLERK_AUTHORIZED_PARTIES")
    clerk_api_url: str = Field("https://api.clerk.com/v1", alias="CLERK_API_URL")

    ai_agents_dir: Path = Field(default=REPO_ROOT / "ai-agents", alias="AI_AGENTS_DIR")
    scraper_agents_dir: Path = Field(
        default=REPO_ROOT / "scraper-agents",
        alias="SCRAPER_AGENTS_DIR",
    )
    runtime_dir: Path = Field(default=BASE_DIR / "runtime", alias="RUNTIME_DIR")
    snapshot_storage_dir: Path = Field(
        default=REPO_ROOT / "scraper-agents" / "snapshots",
        alias="SNAPSHOT_STORAGE_DIR",
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def clerk_jwks_url_resolved(self) -> str:
        if self.clerk_jwks_url:
            return self.clerk_jwks_url
        if not self.clerk_issuer:
            return ""
        return f"{self.clerk_issuer.rstrip('/')}/.well-known/jwks.json"

    @property
    def clerk_authorized_parties_list(self) -> list[str]:
        return [item.strip() for item in self.clerk_authorized_parties.split(",") if item.strip()]


settings = Settings()
