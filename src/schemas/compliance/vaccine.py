from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class VaccineBase(StrictInputSchema):
    """Shared fields for Vaccine schemas."""

    vaccine_name: str = Field(
        max_length=100,
        description="Name of the vaccine",
    )

    disease: str = Field(
        max_length=100,
        description="Disease prevented by the vaccine",
    )


class VaccineCreate(VaccineBase):
    """Schema for creating a vaccine."""

    pass


class VaccineUpdate(StrictInputSchema):
    """Schema for updating a vaccine."""

    vaccine_name: str | None = Field(
        default=None,
        max_length=100,
    )

    disease: str | None = Field(
        default=None,
        max_length=100,
    )

    active: bool | None = None


class VaccineResponse(
    BaseResponseSchema,
    VaccineBase,
):
    """Schema returned for vaccine responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )