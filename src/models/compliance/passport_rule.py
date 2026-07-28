from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.reference.passport_type import PassportType


class PassportRule(BaseModel):
    __tablename__ = "passport_rules"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
        unique=True,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    passport_type_id: Mapped[int] = mapped_column(
        ForeignKey("passport_types.id"),
        nullable=False,
    )

    minimum_validity_months: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    blank_pages_required: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    machine_readable_required: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    damaged_passport_allowed: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    temporary_passport_allowed: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    passport_issue_date_required: Mapped[bool | None] = mapped_column(
        Boolean,
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
        back_populates="passport_rule",
    )

    destination_country: Mapped["Country"] = relationship(
        "Country",
        back_populates="destination_passport_rules",
    )

    passport_type: Mapped["PassportType"] = relationship(
        "PassportType",
        back_populates="passport_rules",
    )