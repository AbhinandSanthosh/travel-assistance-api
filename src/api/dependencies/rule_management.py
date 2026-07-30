from fastapi import Depends

from src.repositories.rule_management.rule_status import (
    RuleStatusRepository,
)
from src.services.rule_management.rule_status import (
    RuleStatusService,
)
from src.repositories.rule_management.rule_version import (
    RuleVersionRepository,
)
from src.services.rule_management.rule_version import (
    RuleVersionService,
)
from src.repositories.rule_management.rule_history import (
    RuleHistoryRepository,
)
from src.services.rule_management.rule_history import (
    RuleHistoryService,
)
from src.services.rule_management.rule_approval import RuleApprovalService
from src.repositories.rule_management.rule_simulation import (
    RuleSimulationRepository,
)
from src.services.rule_management.rule_simulation import (
    RuleSimulationService,
)

def get_rule_status_repository() -> RuleStatusRepository:
    """Get RuleStatus repository instance."""
    return RuleStatusRepository()


def get_rule_status_service(
    rule_status_repository: RuleStatusRepository = Depends(
        get_rule_status_repository,
    ),
) -> RuleStatusService:
    """Get RuleStatus service instance."""
    return RuleStatusService(
        rule_status_repository,
    )

def get_rule_version_repository() -> RuleVersionRepository:
    """Get Rule Version repository."""
    return RuleVersionRepository()


def get_rule_version_service(
    repository: RuleVersionRepository = Depends(
        get_rule_version_repository,
    ),
) -> RuleVersionService:
    """Get Rule Version service."""
    return RuleVersionService(repository)

def get_rule_history_repository() -> RuleHistoryRepository:
    """Get Rule History repository."""
    return RuleHistoryRepository()


def get_rule_history_service(
    repository: RuleHistoryRepository = Depends(
        get_rule_history_repository,
    ),
) -> RuleHistoryService:
    """Get Rule History service."""
    return RuleHistoryService(repository)

def get_rule_approval_service() -> RuleApprovalService:
    """Return a RuleApprovalService instance."""

    return RuleApprovalService()

def get_rule_simulation_repository() -> RuleSimulationRepository:
    """Get Rule Simulation repository."""
    return RuleSimulationRepository()


def get_rule_simulation_service(
    repository: RuleSimulationRepository = Depends(
        get_rule_simulation_repository,
    ),
) -> RuleSimulationService:
    """Get Rule Simulation service."""
    return RuleSimulationService(repository)