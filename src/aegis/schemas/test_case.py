from datetime import datetime

from pydantic import Field

from .base import AegisBaseModel, utc_now
from .enums import TestCategory


class TestCase(AegisBaseModel):
    __test__ = False

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    prompt: str = Field(..., min_length=1)
    category: TestCategory = TestCategory.OTHER
    strategy: str | None = Field(default=None, max_length=200)
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)