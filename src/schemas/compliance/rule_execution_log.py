from pydantic import ConfigDict

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleExecutionLogBase(StrictInputSchema):
    """Base schema for rule execution log."""

    request_id: str
    rule_id: int
    matched: bool
    skipped: bool = False
    execution_time_ms: int
    reason: str | None = None


class RuleExecutionLogCreate(
    RuleExecutionLogBase,
):
    """Schema for creating a rule execution log."""


class RuleExecutionLogUpdate(StrictInputSchema):
    """Schema for updating a rule execution log."""

    request_id: str | None = None
    rule_id: int | None = None
    matched: bool | None = None
    skipped: bool | None = None
    execution_time_ms: int | None = None
    reason: str | None = None


class RuleExecutionLogResponse(
    BaseResponseSchema,
    RuleExecutionLogBase,
):
    """Schema for rule execution log response."""

    model_config = ConfigDict(
        from_attributes=True,
    )