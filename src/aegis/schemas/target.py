from datetime import datetime

from pydantic import Field, HttpUrl

from .base import AegisBaseModel, utc_now
from .enums import TargetKind


class Target(AegisBaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=200)
    kind: TargetKind
    model: str | None = Field(default=None, max_length=200)
    endpoint: HttpUrl | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)