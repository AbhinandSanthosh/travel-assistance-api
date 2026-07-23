from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema
from src.schemas.reference.country import CountryResponse


class TravelAuthorizationBase(BaseModel):
    """Shared fields for TravelAuthorization schemas."""

    authorization_code: str = Field(..., max_length=20)
    authorization_name: str = Field(..., max_length=150)
    destination_country_id: int
    description: str | None = None


class TravelAuthorizationCreate(TravelAuthorizationBase):
    """Schema for creating a travel authorization."""

    pass


class TravelAuthorizationUpdate(BaseModel):
    """Schema for updating a travel authorization."""

    authorization_code: str | None = Field(
        default=None,
        max_length=20,
    )

    authorization_name: str | None = Field(
        default=None,
        max_length=150,
    )

    destination_country_id: int | None = None

    description: str | None = None

    active: bool | None = None


class TravelAuthorizationResponse(
    BaseResponseSchema,
    TravelAuthorizationBase,
):
    """Schema returned for travel authorization responses."""

    destination_country: CountryResponse | None = None

    model_config = ConfigDict(from_attributes=True)