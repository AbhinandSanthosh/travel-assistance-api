from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_travel_authorization_rule_service,
)
from src.db.session import get_db
from src.schemas.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleCreate,
    TravelAuthorizationRuleResponse,
    TravelAuthorizationRuleUpdate,
)
from src.services.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleService,
)

router = APIRouter(
    prefix="/travel-authorization-rules",
    tags=["Travel Authorization Rules"],
)


@router.post(
    "",
    response_model=TravelAuthorizationRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_travel_authorization_rule(
    travel_authorization_rule_data: (
        TravelAuthorizationRuleCreate
    ),
    db: Session = Depends(get_db),
    service: TravelAuthorizationRuleService = Depends(
        get_travel_authorization_rule_service,
    ),
) -> TravelAuthorizationRuleResponse:
    """Create a new travel authorization rule."""
    return service.create_travel_authorization_rule(
        db,
        travel_authorization_rule_data,
    )


@router.get(
    "",
    response_model=list[TravelAuthorizationRuleResponse],
)
def get_all_travel_authorization_rules(
    db: Session = Depends(get_db),
    service: TravelAuthorizationRuleService = Depends(
        get_travel_authorization_rule_service,
    ),
) -> list[TravelAuthorizationRuleResponse]:
    """Retrieve all travel authorization rules."""
    return service.get_all_travel_authorization_rules(
        db,
    )


@router.get(
    "/{travel_authorization_rule_id}",
    response_model=TravelAuthorizationRuleResponse,
)
def get_travel_authorization_rule(
    travel_authorization_rule_id: int,
    db: Session = Depends(get_db),
    service: TravelAuthorizationRuleService = Depends(
        get_travel_authorization_rule_service,
    ),
) -> TravelAuthorizationRuleResponse:
    """Retrieve a travel authorization rule by ID."""
    return service.get_travel_authorization_rule(
        db,
        travel_authorization_rule_id,
    )


@router.put(
    "/{travel_authorization_rule_id}",
    response_model=TravelAuthorizationRuleResponse,
)
def update_travel_authorization_rule(
    travel_authorization_rule_id: int,
    travel_authorization_rule_data: (
        TravelAuthorizationRuleUpdate
    ),
    db: Session = Depends(get_db),
    service: TravelAuthorizationRuleService = Depends(
        get_travel_authorization_rule_service,
    ),
) -> TravelAuthorizationRuleResponse:
    """Update an existing travel authorization rule."""
    return service.update_travel_authorization_rule(
        db=db,
        travel_authorization_rule_id=(
            travel_authorization_rule_id
        ),
        travel_authorization_rule_data=(
            travel_authorization_rule_data
        ),
    )


@router.delete(
    "/{travel_authorization_rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_travel_authorization_rule(
    travel_authorization_rule_id: int,
    db: Session = Depends(get_db),
    service: TravelAuthorizationRuleService = Depends(
        get_travel_authorization_rule_service,
    ),
) -> Response:
    """Delete a travel authorization rule."""
    service.delete_travel_authorization_rule(
        db,
        travel_authorization_rule_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )