from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.data_collection.source_document import (
        SourceDocument,
    )


class DocumentVersion(BaseModel):
    """Document Version model."""

    __tablename__ = "document_versions"

    document_id: Mapped[int] = mapped_column(
        ForeignKey("source_documents.id"),
        nullable=False,
    )

    version_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    effective_date: Mapped[date | None] = mapped_column(
        nullable=True,
    )

    archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    source_document: Mapped["SourceDocument"] = relationship(
        "SourceDocument",
        back_populates="document_versions",
    )