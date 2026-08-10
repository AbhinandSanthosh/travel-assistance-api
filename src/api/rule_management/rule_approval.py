from typing import Annotated
from src.api.dependencies.auth import require_permission

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.dependencies.rule_management import (
    get_rule_approval_service,
)
from src.schemas.rule_management.rule_approval import (
    RuleApprovalCreate,
    RuleApprovalResponse,
)
from src.services.rule_management.rule_approval import RuleApprovalService

router = APIRouter(
    prefix="/rule-approvals",
    tags=["RuleArovals"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("rule_management.write"))],
    response_model=RuleApprovalResponse,
)
def create_rule_approval(
    approval: RuleApprovalCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleApprovalService,
        Depends(get_rule_approval_service),
    ],
):
    """Create a rule approval."""

    return service.create_rule_approval(
        db=db,
        approval_data=approval,
    )


@router.get(
    "",
    response_model=list[RuleApprovalResponse],
)
def get_all_rule_approvals(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleApprovalService,
        Depends(get_rule_approval_service),
    ],
):
    """Return all rule approvals."""

    return service.get_all_rule_approvals(db=db)


@router.get(
    "/{approval_id}",
    response_model=RuleApprovalResponse,
)
def get_rule_approval(
    approval_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleApprovalService,
        Depends(get_rule_approval_service),
    ],
):
    """Return a rule approval by ID."""

    return service.get_rule_approval(
        db=db,
        approval_id=approval_id,
    )


@router.get(
    "/rule/{rule_id}",
    response_model=list[RuleApprovalResponse],
)
def get_rule_approvals_by_rule(
    rule_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        RuleApprovalService,
        Depends(get_rule_approval_service),
    ],
):
    """Return all approvals for a rule."""

    return service.get_rule_approvals_by_rule(
        db=db,
        rule_id=rule_id,
    )