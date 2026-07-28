from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country


class ImmigrationRule(
    Base,
):
    """Immigration requirements for entry into a destination country."""

    __tablename__ = "immigration_rules"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        unique=True,
        nullable=False,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    onward_ticket_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    accommodation_proof_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    proof_of_funds_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    biometric_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    interview_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    arrival_card_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    digital_arrival_card: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    arrival_registration_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
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
        back_populates="immigration_rule",
    )

    destination_country: Mapped["Country"] = relationship(
        back_populates="immigration_rules",
        foreign_keys=[destination_country_id],
    )