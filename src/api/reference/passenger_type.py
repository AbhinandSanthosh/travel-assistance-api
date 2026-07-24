from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_passenger_type_service
from src.db.session import get_db
from src.schemas.reference.passenger_type import (
    PassengerTypeCreate,
    PassengerTypeResponse,
    PassengerTypeUpdate,
)
from src.services.reference.passenger_type_service import (
    PassengerTypeService,
)

router = APIRouter(prefix="/passenger-types", tags=["Passenger Types"])


@router.post(
    "/",
    response_model=PassengerTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_passenger_type(
    passenger_type_data: PassengerTypeCreate,
    db: Annotated[Session, Depends(get_db)],
    passenger_type_service: Annotated[
        PassengerTypeService,
        Depends(get_passenger_type_service),
    ],
):
    """Create a passenger type."""

    return passenger_type_service.create_passenger_type(
        db,
        passenger_type_data,
    )


@router.get(
    "/",
    response_model=list[PassengerTypeResponse],
)
def get_all_passenger_types(
    db: Annotated[Session, Depends(get_db)],
    passenger_type_service: Annotated[
        PassengerTypeService,
        Depends(get_passenger_type_service),
    ],
):
    """Get all passenger types."""

    return passenger_type_service.get_all_passenger_types(db)


@router.get(
    "/{passenger_type_id}",
    response_model=PassengerTypeResponse,
)
def get_passenger_type(
    passenger_type_id: int,
    db: Annotated[Session, Depends(get_db)],
    passenger_type_service: Annotated[
        PassengerTypeService,
        Depends(get_passenger_type_service),
    ],
):
    """Get a passenger type by ID."""

    return passenger_type_service.get_passenger_type(
        db,
        passenger_type_id,
    )


@router.put(
    "/{passenger_type_id}",
    response_model=PassengerTypeResponse,
)
def update_passenger_type(
    passenger_type_id: int,
    passenger_type_data: PassengerTypeUpdate,
    db: Annotated[Session, Depends(get_db)],
    passenger_type_service: Annotated[
        PassengerTypeService,
        Depends(get_passenger_type_service),
    ],
):
    """Update a passenger type."""

    return passenger_type_service.update_passenger_type(
        db,
        passenger_type_id,
        passenger_type_data,
    )


@router.delete(
    "/{passenger_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_passenger_type(
    passenger_type_id: int,
    db: Annotated[Session, Depends(get_db)],
    passenger_type_service: Annotated[
        PassengerTypeService,
        Depends(get_passenger_type_service),
    ],
):
    """Delete a passenger type."""

    passenger_type_service.delete_passenger_type(
        db,
        passenger_type_id,
    )