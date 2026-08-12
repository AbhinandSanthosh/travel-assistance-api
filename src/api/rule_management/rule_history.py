from fastapi import APIRouter, Depends
#from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.rule_management import (
    get_rule_history_service,
)
from src.db.session import get_db
from src.schemas.rule_management.rule_history import (
    RuleHistoryResponse,
)
from src.services.rule_management.rule_history import (
    RuleHistoryService,
)

router = APIRouter(
    prefix="/rule-history",
    tags=["Rule History"],
)


@router.get(
    "",
    response_model=list[RuleHistoryResponse],
)
def get_all_rule_history(
    db: Session = Depends(get_db),
    service: RuleHistoryService = Depends(
        get_rule_history_service,
    ),
) -> list[RuleHistoryResponse]:
    """Retrieve all rule history records."""
    return service.get_all_rule_history(db)


@router.get(
    "/{history_id}",
    response_model=RuleHistoryResponse,
)
def get_rule_history(
    history_id: int,
    db: Session = Depends(get_db),
    service: RuleHistoryService = Depends(
        get_rule_history_service,
    ),
) -> RuleHistoryResponse:
    """Retrieve a rule history record by ID."""
    return service.get_rule_history(
        db,
        history_id,
    )


@router.get(
    "/rule/{rule_id}",
    response_model=list[RuleHistoryResponse],
)
def get_rule_history_by_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    service: RuleHistoryService = Depends(
        get_rule_history_service,
    ),
) -> list[RuleHistoryResponse]:
    """Retrieve history for a specific rule."""
    return service.get_rule_history_by_rule(
        db,
        rule_id,
    )