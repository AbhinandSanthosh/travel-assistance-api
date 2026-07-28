from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_customs_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.customs_rule import (
    CustomsRuleCreate,
    CustomsRuleResponse,
    CustomsRuleUpdate,
)
from src.services.compliance.customs_rule import (
    CustomsRuleService,
)

router = APIRouter(
    prefix="/customs-rules",
    tags=["Customs Rules"],
)


@router.post(
    "",
    response_model=CustomsRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customs_rule(
    customs_rule_data: CustomsRuleCreate,
    db: Session = Depends(get_db),
    service: CustomsRuleService = Depends(
        get_customs_rule_service,
    ),
) -> CustomsRuleResponse:
    """Create a new customs rule."""
    return service.create_customs_rule(
        db,
        customs_rule_data,
    )


@router.get(
    "",
    response_model=list[CustomsRuleResponse],
)
def get_all_customs_rules(
    db: Session = Depends(get_db),
    service: CustomsRuleService = Depends(
        get_customs_rule_service,
    ),
) -> list[CustomsRuleResponse]:
    """Retrieve all customs rules."""
    return service.get_all_customs_rules(
        db,
    )


@router.get(
    "/{customs_rule_id}",
    response_model=CustomsRuleResponse,
)
def get_customs_rule(
    customs_rule_id: int,
    db: Session = Depends(get_db),
    service: CustomsRuleService = Depends(
        get_customs_rule_service,
    ),
) -> CustomsRuleResponse:
    """Retrieve a customs rule by ID."""
    return service.get_customs_rule(
        db,
        customs_rule_id,
    )


@router.put(
    "/{customs_rule_id}",
    response_model=CustomsRuleResponse,
)
def update_customs_rule(
    customs_rule_id: int,
    customs_rule_data: CustomsRuleUpdate,
    db: Session = Depends(get_db),
    service: CustomsRuleService = Depends(
        get_customs_rule_service,
    ),
) -> CustomsRuleResponse:
    """Update an existing customs rule."""
    return service.update_customs_rule(
        db=db,
        customs_rule_id=customs_rule_id,
        customs_rule_data=customs_rule_data,
    )


@router.delete(
    "/{customs_rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customs_rule(
    customs_rule_id: int,
    db: Session = Depends(get_db),
    service: CustomsRuleService = Depends(
        get_customs_rule_service,
    ),
) -> Response:
    """Delete a customs rule."""
    service.delete_customs_rule(
        db,
        customs_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )