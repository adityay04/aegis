from datetime import datetime

from pydantic import Field

from .base import AegisBaseModel, utc_now

class Score(AegisBaseModel):
    id: str = Field(..., min_length=1)
    evaluation_id: str = Field(..., min_length=1)
    severity: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    novelty: float = Field(..., ge=0.0, le=1.0)
    reproducibility: float = Field(..., ge=0.0, le=1.0)
    strategy_effectiveness: float = Field(..., ge=0.0, le=1.0)
    total: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=utc_now)