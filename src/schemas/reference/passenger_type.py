from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class PassengerTypeBase(StrictInputSchema):
    """Shared fields for PassengerType schemas."""

    passenger_type_code: str = Field(
        ...,
        max_length=20,
    )

    passenger_type_name: str = Field(
        ...,
        max_length=100,
    )

    description: str | None = None


class PassengerTypeCreate(PassengerTypeBase):
    """Schema for creating a passenger type."""

    pass


class PassengerTypeUpdate(StrictInputSchema):
    """Schema for updating a passenger type."""

    passenger_type_code: str | None = Field(
        default=None,
        max_length=20,
    )

    passenger_type_name: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = None

    active: bool | None = None


class PassengerTypeResponse(
    BaseResponseSchema,
    PassengerTypeBase,
):
    """Schema returned for passenger type responses."""

    model_config = ConfigDict(from_attributes=True)