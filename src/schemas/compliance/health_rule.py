from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema


class HealthRuleBase(BaseModel):
    """Shared fields for HealthRule schemas."""

    rule_id: int

    destination_country_id: int

    nationality_country_id: int

    health_form_required: bool = False

    quarantine_required: bool = False

    quarantine_days: int | None = Field(
        default=None,
        ge=0,
        description="Number of quarantine days required",
    )

    medical_certificate_required: bool = False

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
        description="Additional notes for the health rule",
    )


class HealthRuleCreate(HealthRuleBase):
    """Schema for creating a health rule."""

    pass


class HealthRuleUpdate(BaseModel):
    """Schema for updating a health rule."""

    rule_id: int | None = None

    destination_country_id: int | None = None

    nationality_country_id: int | None = None

    health_form_required: bool | None = None

    quarantine_required: bool | None = None

    quarantine_days: int | None = Field(
        default=None,
        ge=0,
    )

    medical_certificate_required: bool | None = None

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class HealthRuleResponse(
    BaseResponseSchema,
    HealthRuleBase,
):
    """Schema returned for health rule responses."""

    model_config = ConfigDict(from_attributes=True)