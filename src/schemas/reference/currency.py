from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class CurrencyBase(StrictInputSchema):
    """Shared fields for Currency schemas."""

    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code",
    )

    currency_name: str = Field(
        ...,
        max_length=100,
    )

    currency_symbol: str | None = Field(
        default=None,
        max_length=10,
    )


class CurrencyCreate(CurrencyBase):
    """Schema for creating a currency."""

    pass


class CurrencyUpdate(StrictInputSchema):
    """Schema for updating a currency."""

    currency_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    currency_name: str | None = Field(
        default=None,
        max_length=100,
    )

    currency_symbol: str | None = Field(
        default=None,
        max_length=10,
    )

    active: bool | None = None


class CurrencyResponse(BaseResponseSchema, CurrencyBase):
    """Schema returned for currency responses."""

    model_config = ConfigDict(from_attributes=True)