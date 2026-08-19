from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class VisaRuleBase(StrictInputSchema):
    """Shared fields for VisaRule schemas."""

    rule_id: int

    nationality_country_id: int

    destination_country_id: int

    passport_type_id: int

    visa_type_id: int

    purpose_id: int

    visa_required: bool = False

    visa_on_arrival: bool = False

    evisa_available: bool = False

    max_stay_days: int | None = Field(
        default=None,
        ge=1,
        description="Maximum permitted stay in days",
    )

    multiple_entry: bool = False

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
        description="Additional notes for the visa rule",
    )


class VisaRuleCreate(VisaRuleBase):
    """Schema for creating a visa rule."""

    pass


class VisaRuleUpdate(StrictInputSchema):
    """Schema for updating a visa rule."""

    rule_id: int | None = None

    nationality_country_id: int | None = None

    destination_country_id: int | None = None

    passport_type_id: int | None = None

    visa_type_id: int | None = None

    purpose_id: int | None = None

    visa_required: bool | None = None

    visa_on_arrival: bool | None = None

    evisa_available: bool | None = None

    max_stay_days: int | None = Field(
        default=None,
        ge=1,
    )

    multiple_entry: bool | None = None

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class VisaRuleResponse(BaseResponseSchema, VisaRuleBase):
    """Schema returned for visa rule responses."""

    model_config = ConfigDict(from_attributes=True)