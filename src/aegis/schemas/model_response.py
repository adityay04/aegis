from datetime import datetime

from pydantic import Field

from .base import AegisBaseModel, utc_now


class ModelResponse(AegisBaseModel):
    id: str = Field(..., min_length=1)
    test_case_id: str = Field(..., min_length=1)
    target_id: str = Field(..., min_length=1)
    content: str | None = None
    error: str | None = None
    latency_ms: float | None = Field(default=None, ge=0)
    raw: dict | None = None
    created_at: datetime = Field(default_factory=utc_now)