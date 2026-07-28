from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.compliance.health_rule_vaccine import (
        HealthRuleVaccine,
    )


class HealthRule(
    Base,
):
    """Health requirements for entry into a destination country."""

    __tablename__ = "health_rules"

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

    nationality_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    health_form_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    quarantine_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    quarantine_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    medical_certificate_required: Mapped[
        bool
    ] = mapped_column(
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
        back_populates="health_rule",
    )

    destination_country: Mapped["Country"] = relationship(
        back_populates="destination_health_rules",
        foreign_keys=[destination_country_id],
    )

    nationality_country: Mapped["Country"] = relationship(
        back_populates="nationality_health_rules",
        foreign_keys=[nationality_country_id],
    )

    health_rule_vaccines: Mapped[
        list["HealthRuleVaccine"]
    ] = relationship(
        back_populates="health_rule",
    )