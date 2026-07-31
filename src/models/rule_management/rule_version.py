from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.administration.user import User
    from src.models.rule_management.rule_history import RuleHistory
    from src.models.rule_management.rule_simulation import RuleSimulation
    from src.models.compliance.compliance_check import ComplianceCheck


class RuleVersion(BaseModel):
    """Rule Version model."""

    __tablename__ = "rule_versions"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    version_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    release_notes: Mapped[str | None] = mapped_column(
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

    published_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="rule_versions",
    )

    publisher: Mapped["User"] = relationship(
        "User",
        back_populates="published_rule_versions",
    )

    previous_version_histories: Mapped[list["RuleHistory"]] = relationship(
        "RuleHistory",
        foreign_keys="RuleHistory.previous_version_id",
        back_populates="previous_version",
    )

    new_version_histories: Mapped[list["RuleHistory"]] = relationship(
        "RuleHistory",
        foreign_keys="RuleHistory.new_version_id",
        back_populates="new_version",
    )

    rule_simulations: Mapped[list["RuleSimulation"]] = relationship(
        "RuleSimulation",
        back_populates="rule_version",
    )

    compliance_checks: Mapped[list["ComplianceCheck"]] = relationship(
        "ComplianceCheck",
        back_populates="rule_version",
    )