

from pydantic import ConfigDict

from src.enums.change_type import ChangeType
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleHistoryBase(StrictInputSchema):
    """Shared fields for Rule History schemas."""

    rule_id: int

    previous_version_id: int | None = None

    new_version_id: int | None = None

    change_type: ChangeType

    change_summary: str | None = None

    changed_by: int | None = None


class RuleHistoryResponse(
    BaseResponseSchema,
    RuleHistoryBase,
):
    """Schema returned for Rule History."""

    model_config = ConfigDict(
        from_attributes=True,
    )