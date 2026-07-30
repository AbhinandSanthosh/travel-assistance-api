from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.validation_status import (
    ValidationStatus,
)

if TYPE_CHECKING:
    from src.models.administration.user import User
    from src.models.data_collection.source_document import (
        SourceDocument,
    )


class DocumentValidation(BaseModel):
    """Document Validation model."""

    __tablename__ = "document_validations"

    document_id: Mapped[int] = mapped_column(
        ForeignKey("source_documents.id"),
        nullable=False,
    )

    validator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    validation_status: Mapped[
        ValidationStatus
    ] = mapped_column(
        SQLEnum(ValidationStatus),
        nullable=False,
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    validated_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    source_document: Mapped["SourceDocument"] = relationship(
        "SourceDocument",
        back_populates="document_validations",
    )

    validator: Mapped["User"] = relationship(
        "User",
    )