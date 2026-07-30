from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.extraction_status import (
    ExtractionStatus,
)

if TYPE_CHECKING:
    from src.models.data_collection.source_document import (
        SourceDocument,
    )


class AIExtraction(BaseModel):
    """AI Extraction model."""

    __tablename__ = "ai_extractions"

    document_id: Mapped[int] = mapped_column(
        ForeignKey("source_documents.id"),
        nullable=False,
    )

    extraction_engine: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    extraction_status: Mapped[
        ExtractionStatus
    ] = mapped_column(
        SQLEnum(ExtractionStatus),
        nullable=False,
    )

    confidence_score: Mapped[
        Decimal | None
    ] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    extracted_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    source_document: Mapped[
        "SourceDocument"
    ] = relationship(
        "SourceDocument",
        back_populates="ai_extractions",
    )