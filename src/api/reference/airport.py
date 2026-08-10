from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_airport_service
from src.db.session import get_db
from src.schemas.reference.airport import (
    AirportCreate,
    AirportResponse,
    AirportUpdate,
)
from src.services.reference.airport_service import AirportService

router = APIRouter(
    prefix="/airports",
    tags=["Airports"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=AirportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_airport(
    airport_data: AirportCreate,
    db: Session = Depends(get_db),
    service: AirportService = Depends(get_airport_service),
):
    """Create a new airport."""
    return service.create_airport(
        db,
        airport_data,
    )


@router.get(
    "",
    response_model=list[AirportResponse],
)
def get_airports(
    db: Session = Depends(get_db),
    service: AirportService = Depends(get_airport_service),
):
    """Retrieve all airports."""
    return service.get_all_airports(db)


@router.get(
    "/{airport_id}",
    response_model=AirportResponse,
)
def get_airport(
    airport_id: int,
    db: Session = Depends(get_db),
    service: AirportService = Depends(get_airport_service),
):
    """Retrieve an airport by ID."""
    return service.get_airport(
        db,
        airport_id,
    )


@router.put(
    "/{airport_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=AirportResponse,
)
def update_airport(
    airport_id: int,
    airport_data: AirportUpdate,
    db: Session = Depends(get_db),
    service: AirportService = Depends(get_airport_service),
):
    """Update an airport."""
    return service.update_airport(
        db,
        airport_id,
        airport_data,
    )


@router.delete(
    "/{airport_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_airport(
    airport_id: int,
    db: Session = Depends(get_db),
    service: AirportService = Depends(get_airport_service),
):
    """Delete an airport."""
    service.delete_airport(
        db,
        airport_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )