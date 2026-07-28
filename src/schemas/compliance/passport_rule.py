from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema


class PassportRuleBase(BaseModel):
    """Shared fields for PassportRule schemas."""

    rule_id: int

    destination_country_id: int

    passport_type_id: int

    minimum_validity_months: int | None = Field(
        default=None,
        ge=0,
        description="Minimum passport validity in months",
    )

    blank_pages_required: int | None = Field(
        default=None,
        ge=0,
        description="Minimum blank passport pages required",
    )

    machine_readable_required: bool = False

    damaged_passport_allowed: bool = False

    temporary_passport_allowed: bool = False

    passport_issue_date_required: bool = False

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
        description="Additional notes for the passport rule",
    )


class PassportRuleCreate(PassportRuleBase):
    """Schema for creating a passport rule."""

    pass


class PassportRuleUpdate(BaseModel):
    """Schema for updating a passport rule."""

    rule_id: int | None = None

    destination_country_id: int | None = None

    passport_type_id: int | None = None

    minimum_validity_months: int | None = Field(
        default=None,
        ge=0,
    )

    blank_pages_required: int | None = Field(
        default=None,
        ge=0,
    )

    machine_readable_required: bool | None = None

    damaged_passport_allowed: bool | None = None

    temporary_passport_allowed: bool | None = None

    passport_issue_date_required: bool | None = None

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class PassportRuleResponse(
    BaseResponseSchema,
    PassportRuleBase,
):
    """Schema returned for passport rule responses."""

    model_config = ConfigDict(from_attributes=True)