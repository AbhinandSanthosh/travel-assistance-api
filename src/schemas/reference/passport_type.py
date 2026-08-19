from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class PassportTypeBase(StrictInputSchema):
    """Shared fields for PassportType schemas."""

    passport_code: str = Field(
        ...,
        min_length=1,
        max_length=10,
    )

    passport_name: str = Field(
        ...,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
    )


class PassportTypeCreate(PassportTypeBase):
    """Schema for creating a passport type."""

    pass


class PassportTypeUpdate(StrictInputSchema):
    """Schema for updating a passport type."""

    passport_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=10,
    )

    passport_name: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = None

    active: bool | None = None


class PassportTypeResponse(
    BaseResponseSchema,
    PassportTypeBase,
):
    """Schema returned for passport type responses."""

    model_config = ConfigDict(from_attributes=True)