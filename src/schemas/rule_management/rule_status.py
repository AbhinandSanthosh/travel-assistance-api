from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RuleStatusBase(StrictInputSchema):
    """Shared fields for Rule Status schemas."""

    status_code: str = Field(
        ...,
        max_length=20,
    )

    status_name: str = Field(
        ...,
        max_length=50,
    )

    description: str | None = Field(
        default=None,
    )

    active: bool = Field(
        default=True,
    )


class RuleStatusCreate(RuleStatusBase):
    """Schema for creating a rule status."""

    pass


class RuleStatusUpdate(StrictInputSchema):
    """Schema for updating a rule status."""

    status_code: str | None = Field(
        default=None,
        max_length=20,
    )

    status_name: str | None = Field(
        default=None,
        max_length=50,
    )

    description: str | None = Field(
        default=None,
    )

    active: bool | None = Field(
        default=None,
    )


class RuleStatusResponse(BaseResponseSchema, RuleStatusBase):
    """Schema returned for rule status responses."""

    model_config = ConfigDict(from_attributes=True)