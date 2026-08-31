from datetime import date
from typing import Any

from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class EntryRestrictionBase(StrictInputSchema):
    """Shared fields for EntryRestriction schemas."""

    rule_id: int

    destination_country_id: int

    nationality_country_id: int

    restriction_type: str = Field(
        description="Type of entry restriction",
    )

    reason: str | None = Field(
        default=None,
        description="Reason for the restriction",
    )

    effective_date: date

    expiry_date: date | None = None

    source_id: int

    condition_expression: dict[str, Any] | None = Field(
        default=None,
        description="JSON expression defining rule conditions",
    )

    remarks: str | None = Field(
        default=None,
        description="Additional notes for the entry restriction",
    )


class EntryRestrictionCreate(
    EntryRestrictionBase,
):
    """Schema for creating an entry restriction."""

    pass


class EntryRestrictionUpdate(StrictInputSchema):
    """Schema for updating an entry restriction."""

    rule_id: int | None = None

    destination_country_id: int | None = None

    nationality_country_id: int | None = None

    restriction_type: str | None = None

    reason: str | None = None

    effective_date: date | None = None

    expiry_date: date | None = None

    source_id: int | None = None

    condition_expression: dict[str, Any] | None = None

    remarks: str | None = None

    active: bool | None = None


class EntryRestrictionResponse(
    BaseResponseSchema,
    EntryRestrictionBase,
):
    """Schema returned for entry restriction responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )