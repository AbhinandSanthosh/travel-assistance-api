from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_airline_service
from src.db.session import get_db
from src.schemas.reference.airline import (
    AirlineCreate,
    AirlineResponse,
    AirlineUpdate,
)
from src.services.reference.airline_service import (
    AirlineService,
)

router = APIRouter(
    prefix="/airlines",
    tags=["Airlines"],
)


@router.post(
    "",
    response_model=AirlineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_airline(
    airline_data: AirlineCreate,
    db: Session = Depends(get_db),
    service: AirlineService = Depends(
        get_airline_service,
    ),
):
    return service.create_airline(
        db,
        airline_data,
    )


@router.get(
    "",
    response_model=list[AirlineResponse],
)
def get_all_airlines(
    db: Session = Depends(get_db),
    service: AirlineService = Depends(
        get_airline_service,
    ),
):
    return service.get_all_airlines(db)


@router.get(
    "/{airline_id}",
    response_model=AirlineResponse,
)
def get_airline(
    airline_id: int,
    db: Session = Depends(get_db),
    service: AirlineService = Depends(
        get_airline_service,
    ),
):
    return service.get_airline(
        db,
        airline_id,
    )


@router.put(
    "/{airline_id}",
    response_model=AirlineResponse,
)
def update_airline(
    airline_id: int,
    airline_data: AirlineUpdate,
    db: Session = Depends(get_db),
    service: AirlineService = Depends(
        get_airline_service,
    ),
):
    return service.update_airline(
        db,
        airline_id,
        airline_data,
    )


@router.delete(
    "/{airline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_airline(
    airline_id: int,
    db: Session = Depends(get_db),
    service: AirlineService = Depends(
        get_airline_service,
    ),
):
    service.delete_airline(
        db,
        airline_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )