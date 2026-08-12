from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.enums.subscription_plan import SubscriptionPlan


class ClientSignupRequest(BaseModel):
    """POST /api/v1/client-portal/signup request body.

    This creates the *account* only -- it does not issue an API key.
    The client logs in afterwards and generates a key from the
    dashboard (POST /api/v1/client-portal/api-key), same as Stripe/
    Twilio/OpenAI: signing up and getting a live secret are two
    separate, deliberate steps.
    """

    company_name: str
    client_name: str = Field(..., description="Contact's display name, e.g. 'Jane Doe'.")
    contact_email: EmailStr
    contact_phone: str | None = None
    password: str = Field(..., min_length=8, examples=["********"])


class ClientSignupResponse(BaseModel):
    """POST /api/v1/client-portal/signup response."""

    client_code: str
    company_name: str
    contact_email: EmailStr
    message: str = "Account created. Log in to generate your API key."


class ClientLoginRequest(BaseModel):
    """POST /api/v1/client-portal/login request body."""

    contact_email: EmailStr
    password: str = Field(..., examples=["********"])


class ClientPortalTokenResponse(BaseModel):
    """POST /api/v1/client-portal/login success response.

    A portal session token -- proves "you're an authorized contact for
    this company." It is *not* the API key and cannot be used against
    /autocheck; it only unlocks the portal endpoints below.
    """

    access_token: str = Field(..., serialization_alias="accessToken")
    token_type: str = Field(default="Bearer", serialization_alias="tokenType")
    expires_in: int = Field(..., serialization_alias="expiresIn")

    model_config = ConfigDict(populate_by_name=True)


class ClientPortalMeResponse(BaseModel):
    """GET /api/v1/client-portal/me response."""

    id: int
    client_code: str
    company_name: str
    client_name: str
    contact_email: EmailStr
    subscription_plan: SubscriptionPlan
    status: bool

    model_config = ConfigDict(from_attributes=True)


class GeneratedAPIKeyResponse(BaseModel):
    """POST /api/v1/client-portal/api-key response.

    `api_key` is the full plaintext secret and is only ever returned
    here, at generation time. From then on the portal only ever shows
    the masked prefix/last-four (see APIKeyStatusResponse) -- the
    server itself never stores the full value again.
    """

    api_key: str
    prefix: str
    last_four: str
    created_at: datetime
    warning: str = (
        "Save this key now -- it will not be shown again. "
        "Store it in your application's environment, not in source control."
    )


class APIKeyStatusResponse(BaseModel):
    """GET /api/v1/client-portal/api-key response.

    Masked status for the dashboard: whether a key exists, and if so,
    a display-safe fragment plus timestamps -- never the key itself.
    """

    has_active_key: bool
    masked_key: str | None = None
    created_at: datetime | None = None
    revoked_at: datetime | None = None