from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.data_collection.source_registry import SourceRegistry


class EntryRestriction(BaseModel):
    """Entry restrictions applicable to travellers."""

    __tablename__ = "entry_restrictions"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    nationality_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    restriction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    effective_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("source_registry.id"),
        nullable=False,
    )

    condition_expression: Mapped[
        dict[str, Any] | None
    ] = mapped_column(
        JSONB,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        back_populates="entry_restrictions",
    )

    destination_country: Mapped["Country"] = relationship(
        back_populates="destination_entry_restrictions",
        foreign_keys=[destination_country_id],
    )

    nationality_country: Mapped["Country"] = relationship(
        back_populates="nationality_entry_restrictions",
        foreign_keys=[nationality_country_id],
    )

    source: Mapped["SourceRegistry"] = relationship(
        "SourceRegistry",
        back_populates="entry_restrictions",
    )