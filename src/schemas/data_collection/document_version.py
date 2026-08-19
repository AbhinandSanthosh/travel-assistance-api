from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class DocumentVersionBase(StrictInputSchema):
    """Shared fields for Document Version schemas."""

    document_id: int

    version_number: str = Field(
        ...,
        max_length=20,
    )

    file_hash: str = Field(
        ...,
        max_length=255,
    )

    effective_date: date | None = None

    archived: bool = False


class DocumentVersionCreate(DocumentVersionBase):
    """Schema for creating a document version."""

    pass


class DocumentVersionUpdate(StrictInputSchema):
    """Schema for updating a document version."""

    document_id: int | None = None

    version_number: str | None = Field(
        default=None,
        max_length=20,
    )

    file_hash: str | None = Field(
        default=None,
        max_length=255,
    )

    effective_date: date | None = None

    archived: bool | None = None


class DocumentVersionResponse(
    BaseResponseSchema,
    DocumentVersionBase,
):
    """Schema returned for document version responses."""

    model_config = ConfigDict(from_attributes=True)