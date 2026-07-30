from sqlalchemy.orm import Session

from src.exceptions.rule_management.rule_simulation import (
    RuleSimulationNotFoundError,
)
from src.models.rule_management.rule_simulation import (
    RuleSimulation,
)
from src.repositories.rule_management.rule_simulation import (
    RuleSimulationRepository,
)
from src.schemas.rule_management.rule_simulation import (
    RuleSimulationCreate,
)
from src.services.base_crud_service import BaseCrudService


class RuleSimulationService:
    """Service for Rule Simulation."""

    def __init__(
        self,
        repository: RuleSimulationRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_rule_simulation(
        self,
        db: Session,
        simulation_data: RuleSimulationCreate,
    ) -> RuleSimulation:
        """Create a rule simulation."""

        return self.base_crud.create(
            db=db,
            obj_in=simulation_data,
        )

    def get_rule_simulation(
        self,
        db: Session,
        simulation_id: int,
    ) -> RuleSimulation:
        """Return a rule simulation by ID."""

        simulation = self.base_crud.get_by_id(
            db=db,
            obj_id=simulation_id,
        )

        if simulation is None:
            raise RuleSimulationNotFoundError(
                simulation_id,
            )

        return simulation

    def get_all_rule_simulations(
        self,
        db: Session,
    ) -> list[RuleSimulation]:
        """Return all rule simulations."""

        return self.base_crud.get_all(db=db)

    def get_rule_simulations_by_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleSimulation]:
        """Return all simulations for a rule."""

        return self.repository.get_by_rule_id(
            db=db,
            rule_id=rule_id,
        )

    def get_rule_simulations_by_rule_version(
        self,
        db: Session,
        rule_version_id: int,
    ) -> list[RuleSimulation]:
        """Return all simulations for a rule version."""

        return self.repository.get_by_rule_version(
            db=db,
            rule_version_id=rule_version_id,
        )