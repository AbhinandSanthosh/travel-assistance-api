from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_country_service
from src.db.session import get_db
from src.schemas.reference.country import (
    CountryCreate,
    CountryResponse,
    CountryUpdate,
)
from src.services.reference.country_service import CountryService

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.post(
    "",
    response_model=CountryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_country(
    country_data: CountryCreate,
    db: Session = Depends(get_db),
    service: CountryService = Depends(get_country_service),
) -> CountryResponse:
    """Create a new country."""
    return service.create_country(db, country_data)


@router.get(
    "",
    response_model=list[CountryResponse],
)
def get_all_countries(
    db: Session = Depends(get_db),
    service: CountryService = Depends(get_country_service),
) -> list[CountryResponse]:
    """Retrieve all countries."""
    return service.get_all_countries(db)


@router.get(
    "/{country_id}",
    response_model=CountryResponse,
)
def get_country(
    country_id: int,
    db: Session = Depends(get_db),
    service: CountryService = Depends(get_country_service),
) -> CountryResponse:
    """Retrieve a country by ID."""
    return service.get_country(db, country_id)


@router.put(
    "/{country_id}",
    response_model=CountryResponse,
)
def update_country(
    country_id: int,
    country_data: CountryUpdate,
    db: Session = Depends(get_db),
    service: CountryService = Depends(get_country_service),
) -> CountryResponse:
    """Update an existing country."""
    return service.update_country(
        db=db,
        country_id=country_id,
        country_data=country_data,
    )


@router.delete(
    "/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_country(
    country_id: int,
    db: Session = Depends(get_db),
    service: CountryService = Depends(get_country_service),
) -> Response:
    """Delete a country."""
    service.delete_country(db, country_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)