from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema
from src.schemas.reference.country import CountryResponse


class AirportBase(StrictInputSchema):
    """Shared fields for Airport schemas."""

    airport_name: str = Field(
        ...,
        max_length=200,
    )

    iata_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    icao_code: str | None = Field(
        default=None,
        min_length=4,
        max_length=4,
    )

    city: str = Field(
        ...,
        max_length=100,
    )

    country_id: int = Field(
        ...,
    )

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )

    international: bool = Field(
        default=True,
    )


class AirportCreate(AirportBase):
    """Schema for creating an airport."""

    pass


class AirportUpdate(StrictInputSchema):
    """Schema for updating an airport."""

    airport_name: str | None = Field(
        default=None,
        max_length=200,
    )

    iata_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    icao_code: str | None = Field(
        default=None,
        min_length=4,
        max_length=4,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    

    country_id: int | None = None

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )

    international: bool | None = None

    active: bool | None = None


class AirportResponse(
    BaseResponseSchema,
    AirportBase,
):
    """Schema returned for airport responses."""

    country: CountryResponse | None = None

    model_config = ConfigDict(from_attributes=True)