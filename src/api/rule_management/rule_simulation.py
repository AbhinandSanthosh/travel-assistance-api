from typing import Annotated
from src.api.dependencies.auth import require_permission

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.dependencies.rule_management import (
    get_rule_simulation_service,
)
from src.schemas.rule_management.rule_simulation import (
    RuleSimulationCreate,
    RuleSimulationResponse,
)
from src.services.rule_management.rule_simulation import (
    RuleSimulationService,
)

router = APIRouter(
    prefix="/rule-simulations",
    tags=["Rule Simulations"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("rule_management.write"))],
    response_model=RuleSimulationResponse,
)
def create_rule_simulation(
    simulation: RuleSimulationCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleSimulationService,
        Depends(get_rule_simulation_service),
    ],
):
    """Create a rule simulation."""

    return service.create_rule_simulation(
        db=db,
        simulation_data=simulation,
    )


@router.get(
    "",
    response_model=list[RuleSimulationResponse],
)
def get_all_rule_simulations(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleSimulationService,
        Depends(get_rule_simulation_service),
    ],
):
    """Return all rule simulations."""

    return service.get_all_rule_simulations(db=db)


@router.get(
    "/{simulation_id}",
    response_model=RuleSimulationResponse,
)
def get_rule_simulation(
    simulation_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleSimulationService,
        Depends(get_rule_simulation_service),
    ],
):
    """Return a rule simulation by ID."""

    return service.get_rule_simulation(
        db=db,
        simulation_id=simulation_id,
    )


@router.get(
    "/rule/{rule_id}",
    response_model=list[RuleSimulationResponse],
)
def get_rule_simulations_by_rule(
    rule_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleSimulationService,
        Depends(get_rule_simulation_service),
    ],
):
    """Return all simulations for a rule."""

    return service.get_rule_simulations_by_rule(
        db=db,
        rule_id=rule_id,
    )


@router.get(
    "/rule-version/{rule_version_id}",
    response_model=list[RuleSimulationResponse],
)
def get_rule_simulations_by_rule_version(
    rule_version_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleSimulationService,
        Depends(get_rule_simulation_service),
    ],
):
    """Return all simulations for a rule version."""

    return service.get_rule_simulations_by_rule_version(
        db=db,
        rule_version_id=rule_version_id,
    )