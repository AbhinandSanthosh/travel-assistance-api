from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema


class RuleVersionBase(BaseModel):
    """Shared fields for Rule Version schemas."""

    rule_id: int

    version_number: str = Field(
        ...,
        max_length=20,
        description="Version number (e.g. 1.0.0)",
    )

    release_notes: str | None = None

    effective_date: date

    expiry_date: date | None = None

    published_by: int | None = None

    published_at: datetime | None = None


class RuleVersionCreate(RuleVersionBase):
    """Schema for creating a rule version."""

    pass


class RuleVersionUpdate(BaseModel):
    """Schema for updating a rule version."""

    version_number: str | None = Field(
        default=None,
        max_length=20,
    )

    release_notes: str | None = None

    effective_date: date | None = None

    expiry_date: date | None = None

    published_by: int | None = None

    published_at: datetime | None = None

    active: bool | None = None


class RuleVersionResponse(
    BaseResponseSchema,
    RuleVersionBase,
):
    """Schema returned for rule version responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )