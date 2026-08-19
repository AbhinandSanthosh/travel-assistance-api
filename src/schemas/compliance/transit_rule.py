from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class TransitRuleBase(StrictInputSchema):
    """Shared fields for TransitRule schemas."""

    rule_id: int

    nationality_country_id: int

    transit_country_id: int

    transit_airport_id: int

    transit_visa_required: bool = False

    airside_transit_allowed: bool = False

    baggage_collection_required: bool = False

    overnight_transit_allowed: bool = False

    max_transit_hours: int | None = Field(
        default=None,
        ge=0,
        description="Maximum allowed transit duration in hours",
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
        description="Additional notes for the transit rule",
    )


class TransitRuleCreate(TransitRuleBase):
    """Schema for creating a transit rule."""

    pass


class TransitRuleUpdate(StrictInputSchema):
    """Schema for updating a transit rule."""

    rule_id: int | None = None

    nationality_country_id: int | None = None

    transit_country_id: int | None = None

    transit_airport_id: int | None = None

    transit_visa_required: bool | None = None

    airside_transit_allowed: bool | None = None

    baggage_collection_required: bool | None = None

    overnight_transit_allowed: bool | None = None

    max_transit_hours: int | None = Field(
        default=None,
        ge=0,
    )

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class TransitRuleResponse(
    BaseResponseSchema,
    TransitRuleBase,
):
    """Schema returned for transit rule responses."""

    model_config = ConfigDict(from_attributes=True)