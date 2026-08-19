from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema

from src.enums.collection_status import CollectionStatus
from src.enums.collection_type import CollectionType

class CollectionLogBase(StrictInputSchema):
    """Shared fields for Collection Log schemas."""

    source_id: int

    collection_type: CollectionType = Field(
        ...,
        max_length=50,
    )

    collection_status: CollectionStatus = Field(
        ...,
        max_length=30,
    )

    message: str | None = None

    collected_by: int

    collected_at: datetime


class CollectionLogCreate(CollectionLogBase):
    """Schema for creating a collection log."""

    pass


class CollectionLogUpdate(StrictInputSchema):
    """Schema for updating a collection log."""

    source_id: int | None = None

    collection_type: str | None = Field(
        default=None,
        max_length=50,
    )

    collection_status: CollectionStatus | None = None


    message: str | None = None

    collected_by: int | None = None

    collected_at: datetime | None = None


class CollectionLogResponse(
    BaseResponseSchema,
    CollectionLogBase,
):
    """Schema returned for collection log responses."""

    model_config = ConfigDict(from_attributes=True)