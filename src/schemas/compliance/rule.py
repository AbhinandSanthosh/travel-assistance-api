from pydantic import ConfigDict, Field

from src.enums.rule_type import RuleType
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleBase(StrictInputSchema):
    """Shared fields for Rule schemas."""

    rule_code: str = Field(
        ...,
        max_length=30,
        description="Unique rule identifier",
    )

    rule_type: RuleType

    source_id: int

    status_id: int

    priority: int = Field(
        default=3,
        ge=1,
        description="Rule evaluation priority",
    )

    created_by: int | None = None

    updated_by: int | None = None


class RuleCreate(RuleBase):
    """Schema for creating a rule."""

    pass


class RuleUpdate(StrictInputSchema):
    """Schema for updating a rule."""

    rule_code: str | None = Field(
        default=None,
        max_length=30,
    )

    rule_type: RuleType | None = None

    source_id: int | None = None

    status_id: int | None = None

    priority: int | None = Field(
        default=None,
        ge=1,
    )

    created_by: int | None = None

    updated_by: int | None = None

    active: bool | None = None


class RuleResponse(BaseResponseSchema, RuleBase):
    """Schema returned for rule responses."""

    model_config = ConfigDict(from_attributes=True)