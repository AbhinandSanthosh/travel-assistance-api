from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.enums.extraction_status import (
    ExtractionStatus,
)
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class AIExtractionBase(StrictInputSchema):
    """Base schema for AI extraction."""

    document_id: int
    extraction_engine: str
    extraction_status: ExtractionStatus
    confidence_score: Decimal | None = None
    extracted_at: datetime


class AIExtractionCreate(
    AIExtractionBase,
):
    """Schema for creating an AI extraction."""


class AIExtractionUpdate(StrictInputSchema):
    """Schema for updating an AI extraction."""

    document_id: int | None = None
    extraction_engine: str | None = None
    extraction_status: (
        ExtractionStatus | None
    ) = None
    confidence_score: (
        Decimal | None
    ) = None
    extracted_at: datetime | None = None


class AIExtractionResponse(
    BaseResponseSchema,
    AIExtractionBase,
):
    """Schema for AI extraction response."""

    model_config = ConfigDict(
        from_attributes=True,
    )