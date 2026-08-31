from pydantic import ConfigDict

from src.enums.approval_status import ApprovalStatus
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleApprovalBase(StrictInputSchema):
    """Shared fields for Rule Approval schemas."""

    rule_id: int

    reviewer_id: int

    approval_status: ApprovalStatus

    comments: str | None = None


class RuleApprovalCreate(RuleApprovalBase):
    """Schema for creating a rule approval."""

    pass


class RuleApprovalResponse(
    BaseResponseSchema,
    RuleApprovalBase,
):
    """Schema returned for Rule Approval."""

    model_config = ConfigDict(
        from_attributes=True,
    )