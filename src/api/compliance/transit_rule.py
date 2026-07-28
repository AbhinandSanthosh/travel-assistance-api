from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_transit_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.transit_rule import (
    TransitRuleCreate,
    TransitRuleResponse,
    TransitRuleUpdate,
)
from src.services.compliance.transit_rule import (
    TransitRuleService,
)

router = APIRouter(
    prefix="/transit-rules",
    tags=["Transit Rules"],
)


@router.post(
    "",
    response_model=TransitRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transit_rule(
    transit_rule_data: TransitRuleCreate,
    db: Session = Depends(get_db),
    service: TransitRuleService = Depends(
        get_transit_rule_service,
    ),
) -> TransitRuleResponse:
    """Create a new transit rule."""
    return service.create_transit_rule(
        db,
        transit_rule_data,
    )


@router.get(
    "",
    response_model=list[TransitRuleResponse],
)
def get_all_transit_rules(
    db: Session = Depends(get_db),
    service: TransitRuleService = Depends(
        get_transit_rule_service,
    ),
) -> list[TransitRuleResponse]:
    """Retrieve all transit rules."""
    return service.get_all_transit_rules(
        db,
    )


@router.get(
    "/{transit_rule_id}",
    response_model=TransitRuleResponse,
)
def get_transit_rule(
    transit_rule_id: int,
    db: Session = Depends(get_db),
    service: TransitRuleService = Depends(
        get_transit_rule_service,
    ),
) -> TransitRuleResponse:
    """Retrieve a transit rule by ID."""
    return service.get_transit_rule(
        db,
        transit_rule_id,
    )


@router.put(
    "/{transit_rule_id}",
    response_model=TransitRuleResponse,
)
def update_transit_rule(
    transit_rule_id: int,
    transit_rule_data: TransitRuleUpdate,
    db: Session = Depends(get_db),
    service: TransitRuleService = Depends(
        get_transit_rule_service,
    ),
) -> TransitRuleResponse:
    """Update an existing transit rule."""
    return service.update_transit_rule(
        db=db,
        transit_rule_id=transit_rule_id,
        transit_rule_data=transit_rule_data,
    )


@router.delete(
    "/{transit_rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transit_rule(
    transit_rule_id: int,
    db: Session = Depends(get_db),
    service: TransitRuleService = Depends(
        get_transit_rule_service,
    ),
) -> Response:
    """Delete a transit rule."""
    service.delete_transit_rule(
        db,
        transit_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )