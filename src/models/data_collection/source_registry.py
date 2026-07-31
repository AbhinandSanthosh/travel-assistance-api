from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.source_type import SourceType
from src.enums.update_frequency import UpdateFrequency

if TYPE_CHECKING:
    from src.models.data_collection.collection_log import CollectionLog
    from src.models.data_collection.source_document import SourceDocument
    from src.models.reference.country import Country
    from src.models.compliance.entry_restriction import EntryRestriction
    from src.models.compliance.rule import Rule


class SourceRegistry(BaseModel):
    """Source Registry model."""

    __tablename__ = "source_registry"

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    authority_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    website: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_type: Mapped[SourceType] = mapped_column(
        SQLEnum(SourceType),
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    update_frequency: Mapped[UpdateFrequency | None] = mapped_column(
        SQLEnum(UpdateFrequency),
        nullable=True,
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="source_registries",
    )

    source_documents: Mapped[list["SourceDocument"]] = relationship(
        "SourceDocument",
        back_populates="source_registry",
    )

    collection_logs: Mapped[list["CollectionLog"]] = relationship(
        "CollectionLog",
        back_populates="source_registry",
    )

    rules: Mapped[list["Rule"]] = relationship(
        "Rule",
        back_populates="source",
    )

    entry_restrictions: Mapped[list["EntryRestriction"]] = relationship(
        "EntryRestriction",
        back_populates="source",
    )