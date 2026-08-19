from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class VisaTypeBase(StrictInputSchema):
    """Shared fields for VisaType schemas."""

    visa_code: str = Field(
        ...,
        min_length=1,
        max_length=10,
    )

    visa_name: str = Field(
        ...,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
    )


class VisaTypeCreate(VisaTypeBase):
    """Schema for creating a visa type."""

    pass


class VisaTypeUpdate(StrictInputSchema):
    """Schema for updating a visa type."""

    visa_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=10,
    )

    visa_name: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = None

    active: bool | None = None


class VisaTypeResponse(
    BaseResponseSchema,
    VisaTypeBase,
):
    """Schema returned for visa type responses."""

    model_config = ConfigDict(from_attributes=True)