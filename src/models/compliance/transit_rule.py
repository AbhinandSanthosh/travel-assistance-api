from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.airport import Airport
    from src.models.reference.country import Country


class TransitRule(BaseModel):
    __tablename__ = "transit_rules"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    nationality_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    transit_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    transit_airport_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id"),
        nullable=False,
    )

    transit_visa_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    airside_transit_allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    baggage_collection_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    overnight_transit_allowed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    max_transit_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    condition_expression: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    exemption_expression: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="transit_rules",
    )

    nationality_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[nationality_country_id],
        back_populates="nationality_transit_rules",
    )

    transit_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[transit_country_id],
        back_populates="transit_country_rules",
    )

    transit_airport: Mapped["Airport"] = relationship(
        "Airport",
        back_populates="transit_rules",
    )