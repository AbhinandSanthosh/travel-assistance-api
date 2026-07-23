from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimestampSchema(BaseModel):
    """Common timestamp fields shared across response schemas."""

    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(TimestampSchema):
    """Base response schema with the primary key."""

    id: int

