from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema
from src.schemas.reference.country import CountryResponse


class AirlineBase(BaseModel):
    """Shared fields for Airline schemas."""

    airline_name: str = Field(
        ...,
        max_length=150,
    )

    iata_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )

    icao_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    country_id: int = Field(
        ...,
    )


class AirlineCreate(AirlineBase):
    """Schema for creating an airline."""

    pass


class AirlineUpdate(BaseModel):
    """Schema for updating an airline."""

    airline_name: str | None = Field(
        default=None,
        max_length=150,
    )

    iata_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )

    icao_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    country_id: int | None = None

    active: bool | None = None


class AirlineResponse(
    BaseResponseSchema,
    AirlineBase,
):
    """Schema returned for airline responses."""

    country: CountryResponse | None = None

    model_config = ConfigDict(from_attributes=True)