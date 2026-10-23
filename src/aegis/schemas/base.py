from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict

class AegisBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True,
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)