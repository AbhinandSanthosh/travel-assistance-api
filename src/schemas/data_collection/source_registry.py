from pydantic import BaseModel, ConfigDict, Field

from src.enums.source_type import SourceType
from src.enums.update_frequency import UpdateFrequency
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class SourceRegistryBase(StrictInputSchema):
    """Shared fields for Source Registry schemas."""

    country_id: int

    authority_name: str = Field(
        ...,
        max_length=200,
    )

    website: str

    source_type: SourceType

    language: str | None = Field(
        default=None,
        max_length=50,
    )

    update_frequency: UpdateFrequency | None = None

    contact_email: str | None = Field(
        default=None,
        max_length=150,
    )

    active: bool = True


class SourceRegistryCreate(SourceRegistryBase):
    """Schema for creating a source registry."""

    pass


class SourceRegistryUpdate(StrictInputSchema):
    """Schema for updating a source registry."""

    country_id: int | None = None

    authority_name: str | None = Field(
        default=None,
        max_length=200,
    )

    website: str | None = None

    source_type: SourceType | None = None

    language: str | None = Field(
        default=None,
        max_length=50,
    )

    update_frequency: UpdateFrequency | None = None

    contact_email: str | None = Field(
        default=None,
        max_length=150,
    )

    active: bool | None = None


class SourceRegistryResponse(BaseResponseSchema, SourceRegistryBase):
    """Schema returned for Source Registry responses."""

    model_config = ConfigDict(from_attributes=True)