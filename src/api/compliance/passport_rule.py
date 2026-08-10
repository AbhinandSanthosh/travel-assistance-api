from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_passport_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.passport_rule import (
    PassportRuleCreate,
    PassportRuleResponse,
    PassportRuleUpdate,
)
from src.services.compliance.passport_rule import (
    PassportRuleService,
)

router = APIRouter(
    prefix="/passport-rules",
    tags=["Passport Rules"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=PassportRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_passport_rule(
    passport_rule_data: PassportRuleCreate,
    db: Session = Depends(get_db),
    service: PassportRuleService = Depends(
        get_passport_rule_service,
    ),
) -> PassportRuleResponse:
    """Create a new passport rule."""
    return service.create_passport_rule(
        db,
        passport_rule_data,
    )


@router.get(
    "",
    response_model=list[PassportRuleResponse],
)
def get_all_passport_rules(
    db: Session = Depends(get_db),
    service: PassportRuleService = Depends(
        get_passport_rule_service,
    ),
) -> list[PassportRuleResponse]:
    """Retrieve all passport rules."""
    return service.get_all_passport_rules(
        db,
    )


@router.get(
    "/{passport_rule_id}",
    response_model=PassportRuleResponse,
)
def get_passport_rule(
    passport_rule_id: int,
    db: Session = Depends(get_db),
    service: PassportRuleService = Depends(
        get_passport_rule_service,
    ),
) -> PassportRuleResponse:
    """Retrieve a passport rule by ID."""
    return service.get_passport_rule(
        db,
        passport_rule_id,
    )


@router.put(
    "/{passport_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    response_model=PassportRuleResponse,
)
def update_passport_rule(
    passport_rule_id: int,
    passport_rule_data: PassportRuleUpdate,
    db: Session = Depends(get_db),
    service: PassportRuleService = Depends(
        get_passport_rule_service,
    ),
) -> PassportRuleResponse:
    """Update an existing passport rule."""
    return service.update_passport_rule(
        db=db,
        passport_rule_id=passport_rule_id,
        passport_rule_data=passport_rule_data,
    )


@router.delete(
    "/{passport_rule_id}",
    dependencies=[Depends(require_permission("compliance.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_passport_rule(
    passport_rule_id: int,
    db: Session = Depends(get_db),
    service: PassportRuleService = Depends(
        get_passport_rule_service,
    ),
) -> Response:
    """Delete a passport rule."""
    service.delete_passport_rule(
        db,
        passport_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )