from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class PurposeBase(StrictInputSchema):
    """Shared fields for Purpose schemas."""

    purpose_code: str = Field(
        ...,
        max_length=20,
    )

    purpose_name: str = Field(
        ...,
        max_length=100,
    )

    description: str | None = None


class PurposeCreate(PurposeBase):
    """Schema for creating a purpose."""

    pass


class PurposeUpdate(StrictInputSchema):
    """Schema for updating a purpose."""

    purpose_code: str | None = Field(
        default=None,
        max_length=20,
    )

    purpose_name: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = None

    active: bool | None = None


class PurposeResponse(
    BaseResponseSchema,
    PurposeBase,
):
    """Schema returned for purpose responses."""

    model_config = ConfigDict(from_attributes=True)