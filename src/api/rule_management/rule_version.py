from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.rule_management import (
    get_rule_version_service,
)
from src.db.session import get_db
from src.schemas.rule_management.rule_version import (
    RuleVersionCreate,
    RuleVersionResponse,
    RuleVersionUpdate,
)
from src.services.rule_management.rule_version import (
    RuleVersionService,
)

router = APIRouter(
    prefix="/rule-versions",
    tags=["Rule Versions"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("rule_management.write"))],
    response_model=RuleVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rule_version(
    rule_version_data: RuleVersionCreate,
    db: Session = Depends(get_db),
    service: RuleVersionService = Depends(
        get_rule_version_service,
    ),
) -> RuleVersionResponse:
    """Create a new rule version."""
    return service.create_rule_version(
        db,
        rule_version_data,
    )


@router.get(
    "",
    response_model=list[RuleVersionResponse],
)
def get_all_rule_versions(
    db: Session = Depends(get_db),
    service: RuleVersionService = Depends(
        get_rule_version_service,
    ),
) -> list[RuleVersionResponse]:
    """Retrieve all rule versions."""
    return service.get_all_rule_versions(db)


@router.get(
    "/{rule_version_id}",
    response_model=RuleVersionResponse,
)
def get_rule_version(
    rule_version_id: int,
    db: Session = Depends(get_db),
    service: RuleVersionService = Depends(
        get_rule_version_service,
    ),
) -> RuleVersionResponse:
    """Retrieve a rule version by ID."""
    return service.get_rule_version(
        db,
        rule_version_id,
    )


@router.put(
    "/{rule_version_id}",
    dependencies=[Depends(require_permission("rule_management.write"))],
    response_model=RuleVersionResponse,
)
def update_rule_version(
    rule_version_id: int,
    rule_version_data: RuleVersionUpdate,
    db: Session = Depends(get_db),
    service: RuleVersionService = Depends(
        get_rule_version_service,
    ),
) -> RuleVersionResponse:
    """Update a rule version."""
    return service.update_rule_version(
        db=db,
        rule_version_id=rule_version_id,
        rule_version_data=rule_version_data,
    )


@router.delete(
    "/{rule_version_id}",
    dependencies=[Depends(require_permission("rule_management.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rule_version(
    rule_version_id: int,
    db: Session = Depends(get_db),
    service: RuleVersionService = Depends(
        get_rule_version_service,
    ),
) -> Response:
    """Delete a rule version."""
    service.delete_rule_version(
        db,
        rule_version_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )