from pydantic import ConfigDict

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class HealthRuleVaccineBase(StrictInputSchema):
    """Shared fields for HealthRuleVaccine schemas."""

    health_rule_id: int

    vaccine_id: int

    certificate_required: bool = False

    created_by: int

    updated_by: int


class HealthRuleVaccineCreate(
    HealthRuleVaccineBase,
):
    """Schema for creating a health rule vaccine."""

    pass


class HealthRuleVaccineUpdate(StrictInputSchema):
    """Schema for updating a health rule vaccine."""

    health_rule_id: int | None = None

    vaccine_id: int | None = None

    certificate_required: bool | None = None

    created_by: int | None = None

    updated_by: int | None = None

    active: bool | None = None


class HealthRuleVaccineResponse(
    BaseResponseSchema,
    HealthRuleVaccineBase,
):
    """Schema returned for health rule vaccine responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )