from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema
from src.schemas.reference.country import CountryResponse


class CityBase(StrictInputSchema):
    """Shared fields for City schemas."""

    city_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="IATA city code, e.g. LON, NYC, TYO",
    )

    city_name: str = Field(
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


class CityCreate(CityBase):
    """Schema for creating a city."""

    pass


class CityUpdate(StrictInputSchema):
    """Schema for updating a city."""

    city_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    city_name: str | None = Field(
        default=None,
        max_length=100,
    )

    country_id: int | None = None

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )

    active: bool | None = None


class CityResponse(
    BaseResponseSchema,
    CityBase,
):
    """Schema returned for city responses."""

    country: CountryResponse | None = None

    model_config = ConfigDict(from_attributes=True)