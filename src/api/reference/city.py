from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_city_service
from src.db.session import get_db
from src.schemas.reference.city import (
    CityCreate,
    CityResponse,
    CityUpdate,
)
from src.services.reference.city_service import CityService

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city_data: CityCreate,
    db: Session = Depends(get_db),
    service: CityService = Depends(get_city_service),
):
    """Create a new city."""
    return service.create_city(
        db,
        city_data,
    )


@router.get(
    "",
    response_model=list[CityResponse],
)
def get_cities(
    db: Session = Depends(get_db),
    service: CityService = Depends(get_city_service),
):
    """Retrieve all cities."""
    return service.get_all_cities(db)


@router.get(
    "/{city_id}",
    response_model=CityResponse,
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db),
    service: CityService = Depends(get_city_service),
):
    """Retrieve a city by ID."""
    return service.get_city(
        db,
        city_id,
    )


@router.put(
    "/{city_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=CityResponse,
)
def update_city(
    city_id: int,
    city_data: CityUpdate,
    db: Session = Depends(get_db),
    service: CityService = Depends(get_city_service),
):
    """Update a city."""
    return service.update_city(
        db,
        city_id,
        city_data,
    )


@router.delete(
    "/{city_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
    service: CityService = Depends(get_city_service),
):
    """Delete a city."""
    service.delete_city(
        db,
        city_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )