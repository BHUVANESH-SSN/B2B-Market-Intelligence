from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Market Intelligence API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/market_intelligence"
    redis_url: str = "rediss://default:<upstash-token>@<upstash-host>:6379?ssl_cert_reqs=required"
    upstash_redis_rest_url: str | None = None
    upstash_redis_rest_token: str | None = None
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    ai_agent_enabled: bool = False
    ai_agent_base_url: str | None = None
    ai_agent_analyze_path: str = "/analyze"
    ai_agent_timeout_seconds: int = 60
    db_echo: bool = False
    cors_origins: str = "*"
    job_status_ttl_seconds: int = 86400
    insights_cache_ttl_seconds: int = 300
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
