from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_health_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.health_rule import (
    HealthRuleCreate,
    HealthRuleResponse,
    HealthRuleUpdate,
)
from src.services.compliance.health_rule import (
    HealthRuleService,
)

router = APIRouter(
    prefix="/health-rules",
    tags=["Health Rules"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=HealthRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_health_rule(
    health_rule_data: HealthRuleCreate,
    db: Session = Depends(get_db),
    service: HealthRuleService = Depends(
        get_health_rule_service,
    ),
) -> HealthRuleResponse:
    """Create a new health rule."""
    return service.create_health_rule(
        db,
        health_rule_data,
    )


@router.get(
    "",
    response_model=list[HealthRuleResponse],
)
def get_all_health_rules(
    db: Session = Depends(get_db),
    service: HealthRuleService = Depends(
        get_health_rule_service,
    ),
) -> list[HealthRuleResponse]:
    """Retrieve all health rules."""
    return service.get_all_health_rules(
        db,
    )


@router.get(
    "/{health_rule_id}",
    response_model=HealthRuleResponse,
)
def get_health_rule(
    health_rule_id: int,
    db: Session = Depends(get_db),
    service: HealthRuleService = Depends(
        get_health_rule_service,
    ),
) -> HealthRuleResponse:
    """Retrieve a health rule by ID."""
    return service.get_health_rule(
        db,
        health_rule_id,
    )


@router.put(
    "/{health_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=HealthRuleResponse,
)
def update_health_rule(
    health_rule_id: int,
    health_rule_data: HealthRuleUpdate,
    db: Session = Depends(get_db),
    service: HealthRuleService = Depends(
        get_health_rule_service,
    ),
) -> HealthRuleResponse:
    """Update an existing health rule."""
    return service.update_health_rule(
        db=db,
        health_rule_id=health_rule_id,
        health_rule_data=health_rule_data,
    )


@router.delete(
    "/{health_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_health_rule(
    health_rule_id: int,
    db: Session = Depends(get_db),
    service: HealthRuleService = Depends(
        get_health_rule_service,
    ),
) -> Response:
    """Delete a health rule."""
    service.delete_health_rule(
        db,
        health_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )