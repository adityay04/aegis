from datetime import datetime

from pydantic import Field, model_validator

from .base import AegisBaseModel, utc_now
from .enums import EvaluationStatus, Severity

class Evaluation(AegisBaseModel):
    id: str = Field(..., min_length=1)
    test_case_id: str = Field(..., min_length=1)
    model_response_id: str = Field(..., min_length=1)
    status: EvaluationStatus
    severity: Severity = Severity.INFO
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str | None = Field(default=None, max_length=5000)
    evaluator: str = Field(..., min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def check_status_severity_consistency(self):
        if self.status == EvaluationStatus.PASS and self.severity != Severity.INFO:
            raise ValueError("Passing evaluations should normally have INFO severity")
        return self