from typing import Any

from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class TravelAuthorizationRuleBase(StrictInputSchema):
    """Shared fields for TravelAuthorizationRule schemas."""

    rule_id: int

    authorization_id: int

    nationality_country_id: int

    destination_country_id: int

    passport_type_id: int

    purpose_id: int

    authorization_required: bool = False

    validity_days: int | None = Field(
        default=None,
        ge=1,
        description="Travel authorization validity in days",
    )

    condition_expression: dict[str, Any] | None = Field(
        default=None,
        description="JSON expression defining rule conditions",
    )

    exemption_expression: dict[str, Any] | None = Field(
        default=None,
        description="JSON expression defining exemptions",
    )

    remarks: str | None = Field(
        default=None,
        description="Additional notes for the travel authorization rule",
    )


class TravelAuthorizationRuleCreate(TravelAuthorizationRuleBase):
    """Schema for creating a travel authorization rule."""

    pass


class TravelAuthorizationRuleUpdate(StrictInputSchema):
    """Schema for updating a travel authorization rule."""

    rule_id: int | None = None

    authorization_id: int | None = None

    nationality_country_id: int | None = None

    destination_country_id: int | None = None

    passport_type_id: int | None = None

    purpose_id: int | None = None

    authorization_required: bool | None = None

    validity_days: int | None = Field(
        default=None,
        ge=1,
    )

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class TravelAuthorizationRuleResponse(
    BaseResponseSchema,
    TravelAuthorizationRuleBase,
):
    """Schema returned for travel authorization rule responses."""

    model_config = ConfigDict(from_attributes=True)