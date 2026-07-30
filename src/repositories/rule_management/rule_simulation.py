from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rule_management.rule_simulation import (
    RuleSimulation,
)
from src.repositories.base_repository import BaseRepository


class RuleSimulationRepository(
    BaseRepository[RuleSimulation]
):
    """Repository for Rule Simulation."""

    def __init__(self) -> None:
        super().__init__(RuleSimulation)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleSimulation]:
        """Return all simulations for a rule."""

        return list(
            db.scalars(
                select(RuleSimulation).where(
                    RuleSimulation.rule_id == rule_id
                )
            )
        )

    def get_by_rule_version(
        self,
        db: Session,
        rule_version_id: int,
    ) -> list[RuleSimulation]:
        """Return all simulations for a rule version."""

        return list(
            db.scalars(
                select(RuleSimulation).where(
                    RuleSimulation.rule_version_id
                    == rule_version_id
                )
            )
        )