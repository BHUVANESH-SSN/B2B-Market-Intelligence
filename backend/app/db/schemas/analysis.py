from __future__ import annotations

from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class AnalysisRunRequest(BaseModel):
    competitor_id: UUID
    url: AnyHttpUrl | None = None
    current_html: str | None = None
    previous_html: str | None = None
    history_claims: list[str] = Field(default_factory=list)

    @field_validator("current_html", "previous_html")
    @classmethod
    def normalize_html(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @field_validator("history_claims")
    @classmethod
    def normalize_claims(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item.strip()]


class AnalysisRunResponse(BaseModel):
    job_id: UUID
    status: str


class ScraperResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_html: str
    current_sections: dict[str, list[str]]
    previous_sections: dict[str, list[str]]
    diffs: dict[str, list[str]]
    snapshot_path: str | None = None
    content_hash: str


class AIReportResult(BaseModel):
    metadata: dict
    insights: list[dict]
    recommendations: list[dict]
