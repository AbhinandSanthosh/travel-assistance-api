from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from src.enums.collection_status import CollectionStatus
from src.enums.collection_type import CollectionType
if TYPE_CHECKING:
    from src.models.administration.user import User
    from src.models.data_collection.source_registry import (
        SourceRegistry,
    )


class CollectionLog(BaseModel):
    """Collection Log model."""

    __tablename__ = "collection_logs"

    source_id: Mapped[int] = mapped_column(
        ForeignKey("source_registry.id"),
        nullable=False,
    )

    collection_type: Mapped[CollectionType] = mapped_column(
        SQLEnum(CollectionType),
        nullable=False,
    )

    collection_status: Mapped[CollectionStatus] = mapped_column(
        SQLEnum(CollectionStatus),
        nullable=False,
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    collected_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    collected_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    source_registry: Mapped["SourceRegistry"] = relationship(
        "SourceRegistry",
        back_populates="collection_logs",
    )

    user: Mapped["User"] = relationship(
        "User",
    )