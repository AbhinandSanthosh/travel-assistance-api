from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.rule_type import RuleType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.compliance.visa_rule import VisaRule
    from src.models.compliance.passport_rule import PassportRule
    from src.models.compliance.transit_rule import TransitRule
    from src.models.compliance.health_rule import (
        HealthRule,
    )
    from src.models.compliance.immigration_rule import ImmigrationRule
    from src.models.compliance.customs_rule import CustomsRule
    from src.models.compliance.entry_restriction import EntryRestriction

class Rule(BaseModel):
    __tablename__ = "rules"

    rule_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    rule_type: Mapped[RuleType] = mapped_column(
        Enum(RuleType, name="rule_type_enum"),
        nullable=False,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("source_registry.id"),
        nullable=False,
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("rule_statuses.id"),
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=3,
        server_default="3",
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    visa_rules: Mapped[list["VisaRule"]] = relationship(
        "VisaRule",
        back_populates="rule",
        uselist=False,
    )

    passport_rule: Mapped["PassportRule"] = relationship(
        "PassportRule",
        back_populates="rule",
        uselist=False,
    )

    transit_rule: Mapped["TransitRule"] = relationship(
        "TransitRule",
        back_populates="rule",
        uselist=False,
    )

    health_rule: Mapped["HealthRule"] = relationship(
        back_populates="rule",
        uselist=False,
    )

    immigration_rule: Mapped["ImmigrationRule"] = relationship(
        back_populates="rule",
    )

    customs_rule: Mapped["CustomsRule"] = relationship(
        back_populates="rule",
    )

    entry_restriction: Mapped["EntryRestriction"] = relationship(
        back_populates="rule",
    )

