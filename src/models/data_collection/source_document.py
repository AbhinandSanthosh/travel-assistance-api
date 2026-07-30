from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.document_type import DocumentType

if TYPE_CHECKING:
    from src.models.data_collection.ai_extraction import AIExtraction
    from src.models.data_collection.document_validation import (
        DocumentValidation,
    )
    from src.models.data_collection.document_version import (
        DocumentVersion,
    )
    from src.models.data_collection.source_registry import (
        SourceRegistry,
    )


class SourceDocument(BaseModel):
    """Source Document model."""

    __tablename__ = "source_documents"

    source_id: Mapped[int] = mapped_column(
        ForeignKey("source_registry.id"),
        nullable=False,
    )

    document_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        SQLEnum(DocumentType),
        nullable=False,
    )

    document_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    file_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    source_registry: Mapped["SourceRegistry"] = relationship(
        "SourceRegistry",
        back_populates="source_documents",
    )

    document_versions: Mapped[list["DocumentVersion"]] = relationship(
        "DocumentVersion",
        back_populates="source_document",
    )

    document_validations: Mapped[
        list["DocumentValidation"]
    ] = relationship(
        "DocumentValidation",
        back_populates="source_document",
    )

    ai_extractions: Mapped[list["AIExtraction"]] = relationship(
        "AIExtraction",
        back_populates="source_document",
    )