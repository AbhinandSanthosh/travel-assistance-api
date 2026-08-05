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
    from src.models.compliance.travel_authorization_rule import TravelAuthorizationRule
    from src.models.rule_management.rule_status import RuleStatus
    from src.models.rule_management.rule_version import RuleVersion
    from src.models.rule_management.rule_history import RuleHistory
    from src.models.rule_management.rule_approval import RuleApproval
    from src.models.rule_management.rule_simulation import RuleSimulation
    from src.models.compliance.rule_execution_log import (
        RuleExecutionLog,
    )
    from src.models.data_collection.source_registry import SourceRegistry

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

    visa_rules: Mapped["VisaRule"] = relationship(
        "VisaRule",
        back_populates="rule",
    )

    passport_rules: Mapped[list["PassportRule"]] = relationship(
        "PassportRule",
        back_populates="rule",
    )

    transit_rules: Mapped[list["TransitRule"]] = relationship(
        "TransitRule",
        back_populates="rule",
    )

    health_rules: Mapped[list["HealthRule"]] = relationship(
        "HealthRule",
        back_populates="rule",
    )

    immigration_rules: Mapped[list["ImmigrationRule"]] = relationship(
        "ImmigrationRule",
        back_populates="rule",
    )

    customs_rules: Mapped[list["CustomsRule"]] = relationship(
        "CustomsRule",
        back_populates="rule",
    )

    entry_restrictions: Mapped[list["EntryRestriction"]] = relationship(
        "EntryRestriction",
        back_populates="rule",
    )

    travel_authorization_rules: Mapped[list["TravelAuthorizationRule"]] = relationship(
        "TravelAuthorizationRule",
        back_populates="rule",
    )

    status: Mapped["RuleStatus"] = relationship(
        "RuleStatus",
        back_populates="rules",
    )

    rule_versions: Mapped[list["RuleVersion"]] = relationship(
        "RuleVersion",
        back_populates="rule",
    )

    rule_history: Mapped[list["RuleHistory"]] = relationship(
        "RuleHistory",
        back_populates="rule",
    )

    rule_approvals: Mapped[list["RuleApproval"]] = relationship(
        "RuleApproval",
        back_populates="rule",
    )

    rule_simulations: Mapped[list["RuleSimulation"]] = relationship(
        "RuleSimulation",
        back_populates="rule",
    )

    rule_execution_logs: Mapped[
        list["RuleExecutionLog"]
    ] = relationship(
        "RuleExecutionLog",
        back_populates="rule",
    )

    source: Mapped["SourceRegistry"] = relationship(
        "SourceRegistry",
        back_populates="rules",
    )

