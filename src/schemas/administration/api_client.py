from datetime import datetime

from pydantic import ConfigDict, EmailStr

from src.enums.subscription_plan import SubscriptionPlan
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class APIClientBase(StrictInputSchema):
    """Shared fields for API Client schemas."""

    client_name: str

    company_name: str

    client_code: str

    api_key: str | None = None

    contact_name: str | None = None

    contact_email: EmailStr

    contact_phone: str | None = None

    subscription_plan: SubscriptionPlan

    requests_per_minute: int = 60

    status: bool = True

    expires_at: datetime | None = None


class APIClientCreate(APIClientBase):
    """Schema for creating an API client."""

    pass


class APIClientUpdate(StrictInputSchema):
    """Schema for updating an API client."""

    client_name: str | None = None

    company_name: str | None = None

    client_code: str | None = None

    api_key: str | None = None

    contact_name: str | None = None

    contact_email: EmailStr | None = None

    contact_phone: str | None = None

    subscription_plan: SubscriptionPlan | None = None

    requests_per_minute: int | None = None

    status: bool | None = None

    expires_at: datetime | None = None


class APIClientResponse(
    BaseResponseSchema,
    APIClientBase,
):
    """Schema returned for API Client (admin console).

    Never exposes api_key_hash or contact_password_hash -- only the
    masked prefix/last-four, same as the portal's own /api-key status
    endpoint.
    """

    api_key_prefix: str | None = None
    api_key_last_four: str | None = None
    api_key_created_at: datetime | None = None
    api_key_revoked_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )