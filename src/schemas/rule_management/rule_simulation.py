from typing import Any

from pydantic import BaseModel, ConfigDict

from src.enums.simulation_status import SimulationStatus
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleSimulationBase(StrictInputSchema):
    """Shared fields for Rule Simulation schemas."""

    simulation_name: str

    rule_id: int

    rule_version_id: int

    request_payload: dict[str, Any]

    expected_result: dict[str, Any]

    actual_result: dict[str, Any] | None = None

    simulation_status: SimulationStatus

    executed_by: int

    remarks: str | None = None


class RuleSimulationCreate(RuleSimulationBase):
    """Schema for creating a rule simulation."""

    pass


class RuleSimulationResponse(
    BaseResponseSchema,
    RuleSimulationBase,
):
    """Schema returned for Rule Simulation."""

    model_config = ConfigDict(
        from_attributes=True,
    )