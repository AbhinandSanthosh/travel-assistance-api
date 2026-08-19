from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RegionBase(StrictInputSchema):
    """Shared fields for Region schemas."""

    region_name: str = Field(
        ...,
        max_length=100,
    )
    description: str | None = None


class RegionCreate(RegionBase):
    """Schema for creating a region."""

    pass


class RegionUpdate(StrictInputSchema):
    """Schema for updating a region."""

    region_name: str | None = Field(
        default=None,
        max_length=100,
    )
    description: str | None = None
    active: bool | None = None


class RegionResponse(BaseResponseSchema, RegionBase):
    """Schema returned for region responses."""

    model_config = ConfigDict(from_attributes=True)