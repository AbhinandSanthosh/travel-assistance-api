from typing import Annotated
from src.api.dependencies.auth import require_permission

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_travel_authorization_service
from src.db.session import get_db
from src.schemas.reference.travel_authorization import (
    TravelAuthorizationCreate,
    TravelAuthorizationResponse,
    TravelAuthorizationUpdate,
)
from src.services.reference.travel_authorization_service import (
    TravelAuthorizationService,
)

router = APIRouter(
    prefix="/travel-authorizations",
    tags=["Travel Authorizations"],
)


@router.post(
    "/",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=TravelAuthorizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_travel_authorization(
    travel_authorization_data: TravelAuthorizationCreate,
    db: Annotated[Session, Depends(get_db)],
    travel_authorization_service: Annotated[
        TravelAuthorizationService,
        Depends(get_travel_authorization_service),
    ],
):
    """Create a travel authorization."""

    return travel_authorization_service.create_travel_authorization(
        db,
        travel_authorization_data,
    )


@router.get(
    "/",
    response_model=list[TravelAuthorizationResponse],
)
def get_all_travel_authorizations(
    db: Annotated[Session, Depends(get_db)],
    travel_authorization_service: Annotated[
        TravelAuthorizationService,
        Depends(get_travel_authorization_service),
    ],
):
    """Get all travel authorizations."""

    return (
        travel_authorization_service.get_all_travel_authorizations(
            db,
        )
    )


@router.get(
    "/{travel_authorization_id}",
    response_model=TravelAuthorizationResponse,
)
def get_travel_authorization(
    travel_authorization_id: int,
    db: Annotated[Session, Depends(get_db)],
    travel_authorization_service: Annotated[
        TravelAuthorizationService,
        Depends(get_travel_authorization_service),
    ],
):
    """Get a travel authorization by ID."""

    return travel_authorization_service.get_travel_authorization(
        db,
        travel_authorization_id,
    )


@router.put(
    "/{travel_authorization_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=TravelAuthorizationResponse,
)
def update_travel_authorization(
    travel_authorization_id: int,
    travel_authorization_data: TravelAuthorizationUpdate,
    db: Annotated[Session, Depends(get_db)],
    travel_authorization_service: Annotated[
        TravelAuthorizationService,
        Depends(get_travel_authorization_service),
    ],
):
    """Update a travel authorization."""

    return (
        travel_authorization_service.update_travel_authorization(
            db,
            travel_authorization_id,
            travel_authorization_data,
        )
    )


@router.delete(
    "/{travel_authorization_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_travel_authorization(
    travel_authorization_id: int,
    db: Annotated[Session, Depends(get_db)],
    travel_authorization_service: Annotated[
        TravelAuthorizationService,
        Depends(get_travel_authorization_service),
    ],
):
    """Delete a travel authorization."""

    travel_authorization_service.delete_travel_authorization(
        db,
        travel_authorization_id,
    )