from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import get_rule_service
from src.db.session import get_db
from src.schemas.compliance.rule import (
    RuleCreate,
    RuleResponse,
    RuleUpdate,
)
from src.services.compliance.rule import RuleService

router = APIRouter(
    prefix="/rules",
    tags=["Rules"],
)


@router.post(
    "",
    response_model=RuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rule(
    rule_data: RuleCreate,
    db: Session = Depends(get_db),
    service: RuleService = Depends(get_rule_service),
) -> RuleResponse:
    """Create a new rule."""
    return service.create_rule(db, rule_data)


@router.get(
    "",
    response_model=list[RuleResponse],
)
def get_all_rules(
    db: Session = Depends(get_db),
    service: RuleService = Depends(get_rule_service),
) -> list[RuleResponse]:
    """Retrieve all rules."""
    return service.get_all_rules(db)


@router.get(
    "/{rule_id}",
    response_model=RuleResponse,
)
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    service: RuleService = Depends(get_rule_service),
) -> RuleResponse:
    """Retrieve a rule by ID."""
    return service.get_rule(db, rule_id)


@router.put(
    "/{rule_id}",
    response_model=RuleResponse,
)
def update_rule(
    rule_id: int,
    rule_data: RuleUpdate,
    db: Session = Depends(get_db),
    service: RuleService = Depends(get_rule_service),
) -> RuleResponse:
    """Update an existing rule."""
    return service.update_rule(
        db=db,
        rule_id=rule_id,
        rule_data=rule_data,
    )


@router.delete(
    "/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    service: RuleService = Depends(get_rule_service),
) -> Response:
    """Delete a rule."""
    service.delete_rule(db, rule_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )