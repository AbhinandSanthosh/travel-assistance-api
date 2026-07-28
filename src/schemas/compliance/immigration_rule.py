from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema


class ImmigrationRuleBase(BaseModel):
    """Shared fields for ImmigrationRule schemas."""

    rule_id: int

    destination_country_id: int

    onward_ticket_required: bool = False

    accommodation_proof_required: bool = False

    proof_of_funds_required: bool = False

    biometric_required: bool = False

    interview_required: bool = False

    arrival_card_required: bool = False

    digital_arrival_card: bool = False

    arrival_registration_required: bool = False

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
        description="Additional notes for the immigration rule",
    )


class ImmigrationRuleCreate(ImmigrationRuleBase):
    """Schema for creating an immigration rule."""

    pass


class ImmigrationRuleUpdate(BaseModel):
    """Schema for updating an immigration rule."""

    rule_id: int | None = None

    destination_country_id: int | None = None

    onward_ticket_required: bool | None = None

    accommodation_proof_required: bool | None = None

    proof_of_funds_required: bool | None = None

    biometric_required: bool | None = None

    interview_required: bool | None = None

    arrival_card_required: bool | None = None

    digital_arrival_card: bool | None = None

    arrival_registration_required: bool | None = None

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class ImmigrationRuleResponse(
    BaseResponseSchema,
    ImmigrationRuleBase,
):
    """Schema returned for immigration rule responses."""

    model_config = ConfigDict(from_attributes=True)