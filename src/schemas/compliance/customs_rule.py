from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class CustomsRuleBase(StrictInputSchema):
    """Shared fields for CustomsRule schemas."""

    rule_id: int

    destination_country_id: int

    nationality_country_id: int

    alcohol_limit: str | None = Field(
        default=None,
        description="Allowed alcohol limit",
    )

    tobacco_limit: str | None = Field(
        default=None,
        description="Allowed tobacco limit",
    )

    currency_limit_amount: Decimal | None = Field(
        default=None,
        ge=0,
        description="Maximum currency amount allowed",
    )

    currency_id: int | None = None

    currency_declaration_required: bool = False

    medication_rules: str | None = Field(
        default=None,
        description="Medication import rules",
    )

    prohibited_items: str | None = Field(
        default=None,
        description="List of prohibited items",
    )

    restricted_items: str | None = Field(
        default=None,
        description="List of restricted items",
    )

    pet_import_rules: str | None = Field(
        default=None,
        description="Pet import requirements",
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
        description="Additional notes for the customs rule",
    )


class CustomsRuleCreate(CustomsRuleBase):
    """Schema for creating a customs rule."""

    pass


class CustomsRuleUpdate(StrictInputSchema):
    """Schema for updating a customs rule."""

    rule_id: int | None = None

    destination_country_id: int | None = None

    nationality_country_id: int | None = None

    alcohol_limit: str | None = None

    tobacco_limit: str | None = None

    currency_limit_amount: Decimal | None = Field(
        default=None,
        ge=0,
    )

    currency_id: int | None = None

    currency_declaration_required: bool | None = None

    medication_rules: str | None = None

    prohibited_items: str | None = None

    restricted_items: str | None = None

    pet_import_rules: str | None = None

    condition_expression: dict[str, Any] | None = None

    exemption_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class CustomsRuleResponse(
    BaseResponseSchema,
    CustomsRuleBase,
):
    """Schema returned for customs rule responses."""

    model_config = ConfigDict(from_attributes=True)