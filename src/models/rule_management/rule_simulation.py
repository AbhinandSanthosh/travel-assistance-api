from typing import TYPE_CHECKING, Any

from sqlalchemy import Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.db.base_model import BaseModel
from src.enums.simulation_status import SimulationStatus

if TYPE_CHECKING:
    from src.models.administration.user import User
    from src.models.compliance.rule import Rule
    from src.models.rule_management.rule_version import RuleVersion


class RuleSimulation(BaseModel):
    """Rule Simulation model."""

    __tablename__ = "rule_simulations"

    simulation_name: Mapped[str] = mapped_column(
        nullable=False,
    )

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    rule_version_id: Mapped[int] = mapped_column(
        ForeignKey("rule_versions.id"),
        nullable=False,
    )

    request_payload: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    expected_result: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )

    actual_result: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    simulation_status: Mapped[SimulationStatus] = mapped_column(
        Enum(
            SimulationStatus,
            name="simulation_status_enum",
        ),
        nullable=False,
    )

    executed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    executed_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="rule_simulations",
    )

    rule_version: Mapped["RuleVersion"] = relationship(
        "RuleVersion",
        back_populates="rule_simulations",
    )

    executor: Mapped["User"] = relationship(
        "User",
        back_populates="rule_simulations",
    )