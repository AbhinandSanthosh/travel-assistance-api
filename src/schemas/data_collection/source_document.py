from datetime import datetime

from pydantic import ConfigDict, Field

from src.enums.document_type import DocumentType
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class SourceDocumentBase(StrictInputSchema):
    """Shared fields for Source Document schemas."""

    source_id: int

    document_name: str = Field(
        ...,
        max_length=255,
    )

    document_type: DocumentType

    document_url: str

    file_hash: str = Field(
        ...,
        max_length=255,
    )

    downloaded_at: datetime


class SourceDocumentCreate(SourceDocumentBase):
    """Schema for creating a source document."""

    pass


class SourceDocumentUpdate(StrictInputSchema):
    """Schema for updating a source document."""

    source_id: int | None = None

    document_name: str | None = Field(
        default=None,
        max_length=255,
    )

    document_type: DocumentType | None = None

    document_url: str | None = None

    file_hash: str | None = Field(
        default=None,
        max_length=255,
    )

    downloaded_at: datetime | None = None


class SourceDocumentResponse(
    BaseResponseSchema,
    SourceDocumentBase,
):
    """Schema returned for source document responses."""

    model_config = ConfigDict(from_attributes=True)