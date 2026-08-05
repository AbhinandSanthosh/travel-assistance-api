from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.reference.currency import Currency


class CustomsRule(BaseModel):
    """Customs requirements for entry into a destination country."""

    __tablename__ = "customs_rules"

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

    alcohol_limit: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tobacco_limit: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    currency_limit_amount: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    currency_id: Mapped[int | None] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=True,
    )

    currency_declaration_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    medication_rules: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    prohibited_items: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    restricted_items: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pet_import_rules: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    condition_expression: Mapped[
        dict[str, Any] | None
    ] = mapped_column(
        JSONB,
        nullable=True,
    )

    exemption_expression: Mapped[
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
        back_populates="customs_rules",
    )

    destination_country: Mapped["Country"] = relationship(
        back_populates="destination_customs_rules",
        foreign_keys=[destination_country_id],
    )

    nationality_country: Mapped["Country"] = relationship(
        back_populates="nationality_customs_rules",
        foreign_keys=[nationality_country_id],
    )

    currency: Mapped["Currency"] = relationship(
        back_populates="customs_rules",
    )