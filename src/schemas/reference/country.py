

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema


class CountryBase(BaseModel):
    """Shared fields for Country schemas."""

    iso2: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code",
    )
    iso3: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 3166-1 alpha-3 country code",
    )
    country_name: str = Field(
        ...,
        max_length=100,
    )
    nationality: str = Field(
        ...,
        max_length=100,
    )
    region_id: int
    capital: str | None = Field(
        default=None,
        max_length=100,
    )
    currency_id: int
    official_language: str | None = Field(
        default=None,
        max_length=100,
    )
    timezone: str | None = Field(
        default=None,
        max_length=100,
    )


class CountryCreate(CountryBase):
    """Schema for creating a country."""

    pass


class CountryUpdate(BaseModel):
    """Schema for updating a country."""

    iso2: str | None = Field(default=None, min_length=2, max_length=2)
    iso3: str | None = Field(default=None, min_length=3, max_length=3)
    country_name: str | None = Field(default=None, max_length=100)
    nationality: str | None = Field(default=None, max_length=100)
    region_id: int | None = None
    capital: str | None = Field(default=None, max_length=100)
    currency_id: int | None = None
    official_language: str | None = Field(default=None, max_length=100)
    timezone: str | None = Field(default=None, max_length=100)
    active: bool | None = None


class CountryResponse(BaseResponseSchema, CountryBase):
    """Schema returned for country responses."""

    model_config = ConfigDict(from_attributes=True)