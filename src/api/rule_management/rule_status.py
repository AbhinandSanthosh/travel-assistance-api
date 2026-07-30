from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.rule_management import (
    get_rule_status_service,
)
from src.db.session import get_db

from src.schemas.rule_management.rule_status import (
    RuleStatusCreate,
    RuleStatusResponse,
    RuleStatusUpdate,
)

from src.services.rule_management.rule_status import (
    RuleStatusService,
)

router = APIRouter(
    prefix="/rule-statuses",
    tags=["Rule Statuses"],
)


@router.post(
    "",
    response_model=RuleStatusResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rule_status(
    rule_status_data: RuleStatusCreate,
    db: Session = Depends(get_db),
    service: RuleStatusService = Depends(
        get_rule_status_service,
    ),
) -> RuleStatusResponse:
    """Create a new rule status."""
    return service.create_rule_status(
        db,
        rule_status_data,
    )


@router.get(
    "",
    response_model=list[RuleStatusResponse],
)
def get_all_rule_statuses(
    db: Session = Depends(get_db),
    service: RuleStatusService = Depends(
        get_rule_status_service,
    ),
) -> list[RuleStatusResponse]:
    """Retrieve all rule statuses."""
    return service.get_all_rule_statuses(db)


@router.get(
    "/{rule_status_id}",
    response_model=RuleStatusResponse,
)
def get_rule_status(
    rule_status_id: int,
    db: Session = Depends(get_db),
    service: RuleStatusService = Depends(
        get_rule_status_service,
    ),
) -> RuleStatusResponse:
    """Retrieve a rule status by ID."""
    return service.get_rule_status(
        db,
        rule_status_id,
    )


@router.put(
    "/{rule_status_id}",
    response_model=RuleStatusResponse,
)
def update_rule_status(
    rule_status_id: int,
    rule_status_data: RuleStatusUpdate,
    db: Session = Depends(get_db),
    service: RuleStatusService = Depends(
        get_rule_status_service,
    ),
) -> RuleStatusResponse:
    """Update an existing rule status."""
    return service.update_rule_status(
        db=db,
        rule_status_id=rule_status_id,
        rule_status_data=rule_status_data,
    )


@router.delete(
    "/{rule_status_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rule_status(
    rule_status_id: int,
    db: Session = Depends(get_db),
    service: RuleStatusService = Depends(
        get_rule_status_service,
    ),
) -> Response:
    """Delete a rule status."""
    service.delete_rule_status(
        db,
        rule_status_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )