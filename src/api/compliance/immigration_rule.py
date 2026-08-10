from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_immigration_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.immigration_rule import (
    ImmigrationRuleCreate,
    ImmigrationRuleResponse,
    ImmigrationRuleUpdate,
)
from src.services.compliance.immigration_rule import (
    ImmigrationRuleService,
)

router = APIRouter(
    prefix="/immigration-rules",
    tags=["Immigration Rules"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=ImmigrationRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_immigration_rule(
    immigration_rule_data: ImmigrationRuleCreate,
    db: Session = Depends(get_db),
    service: ImmigrationRuleService = Depends(
        get_immigration_rule_service,
    ),
) -> ImmigrationRuleResponse:
    """Create a new immigration rule."""
    return service.create_immigration_rule(
        db,
        immigration_rule_data,
    )


@router.get(
    "",
    response_model=list[ImmigrationRuleResponse],
)
def get_all_immigration_rules(
    db: Session = Depends(get_db),
    service: ImmigrationRuleService = Depends(
        get_immigration_rule_service,
    ),
) -> list[ImmigrationRuleResponse]:
    """Retrieve all immigration rules."""
    return service.get_all_immigration_rules(
        db,
    )


@router.get(
    "/{immigration_rule_id}",
    response_model=ImmigrationRuleResponse,
)
def get_immigration_rule(
    immigration_rule_id: int,
    db: Session = Depends(get_db),
    service: ImmigrationRuleService = Depends(
        get_immigration_rule_service,
    ),
) -> ImmigrationRuleResponse:
    """Retrieve an immigration rule by ID."""
    return service.get_immigration_rule(
        db,
        immigration_rule_id,
    )


@router.put(
    "/{immigration_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=ImmigrationRuleResponse,
)
def update_immigration_rule(
    immigration_rule_id: int,
    immigration_rule_data: ImmigrationRuleUpdate,
    db: Session = Depends(get_db),
    service: ImmigrationRuleService = Depends(
        get_immigration_rule_service,
    ),
) -> ImmigrationRuleResponse:
    """Update an existing immigration rule."""
    return service.update_immigration_rule(
        db=db,
        immigration_rule_id=immigration_rule_id,
        immigration_rule_data=immigration_rule_data,
    )


@router.delete(
    "/{immigration_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_immigration_rule(
    immigration_rule_id: int,
    db: Session = Depends(get_db),
    service: ImmigrationRuleService = Depends(
        get_immigration_rule_service,
    ),
) -> Response:
    """Delete an immigration rule."""
    service.delete_immigration_rule(
        db,
        immigration_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )