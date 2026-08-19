from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.enums.validation_status import (
    ValidationStatus,
)
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class DocumentValidationBase(StrictInputSchema):
    """Base schema for document validation."""

    document_id: int
    validator_id: int
    validation_status: ValidationStatus
    comments: str | None = None
    validated_at: datetime


class DocumentValidationCreate(
    DocumentValidationBase,
):
    """Schema for creating a document validation."""


class DocumentValidationUpdate(StrictInputSchema):
    """Schema for updating a document validation."""

    document_id: int | None = None
    validator_id: int | None = None
    validation_status: (
        ValidationStatus | None
    ) = None
    comments: str | None = None
    validated_at: datetime | None = None


class DocumentValidationResponse(
    BaseResponseSchema,
    DocumentValidationBase,
):
    """Schema for document validation response."""

    model_config = ConfigDict(
        from_attributes=True,
    )