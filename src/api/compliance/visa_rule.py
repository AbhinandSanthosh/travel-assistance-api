from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import get_visa_rule_service
from src.db.session import get_db
from src.schemas.compliance.visa_rule import (
    VisaRuleCreate,
    VisaRuleResponse,
    VisaRuleUpdate,
)
from src.services.compliance.visa_rule import VisaRuleService

router = APIRouter(
    prefix="/visa-rules",
    tags=["Visa Rules"],
)


@router.post(
    "",
    response_model=VisaRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visa_rule(
    visa_rule_data: VisaRuleCreate,
    db: Session = Depends(get_db),
    service: VisaRuleService = Depends(get_visa_rule_service),
) -> VisaRuleResponse:
    """Create a new visa rule."""
    return service.create_visa_rule(
        db,
        visa_rule_data,
    )


@router.get(
    "",
    response_model=list[VisaRuleResponse],
)
def get_all_visa_rules(
    db: Session = Depends(get_db),
    service: VisaRuleService = Depends(get_visa_rule_service),
) -> list[VisaRuleResponse]:
    """Retrieve all visa rules."""
    return service.get_all_visa_rules(db)


@router.get(
    "/{visa_rule_id}",
    response_model=VisaRuleResponse,
)
def get_visa_rule(
    visa_rule_id: int,
    db: Session = Depends(get_db),
    service: VisaRuleService = Depends(get_visa_rule_service),
) -> VisaRuleResponse:
    """Retrieve a visa rule by ID."""
    return service.get_visa_rule(
        db,
        visa_rule_id,
    )


@router.put(
    "/{visa_rule_id}",
    response_model=VisaRuleResponse,
)
def update_visa_rule(
    visa_rule_id: int,
    visa_rule_data: VisaRuleUpdate,
    db: Session = Depends(get_db),
    service: VisaRuleService = Depends(get_visa_rule_service),
) -> VisaRuleResponse:
    """Update an existing visa rule."""
    return service.update_visa_rule(
        db=db,
        visa_rule_id=visa_rule_id,
        visa_rule_data=visa_rule_data,
    )


@router.delete(
    "/{visa_rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_visa_rule(
    visa_rule_id: int,
    db: Session = Depends(get_db),
    service: VisaRuleService = Depends(get_visa_rule_service),
) -> Response:
    """Delete a visa rule."""
    service.delete_visa_rule(
        db,
        visa_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )