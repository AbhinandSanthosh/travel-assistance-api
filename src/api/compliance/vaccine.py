from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_vaccine_service,
)
from src.db.session import get_db
from src.schemas.compliance.vaccine import (
    VaccineCreate,
    VaccineResponse,
    VaccineUpdate,
)
from src.services.compliance.vaccine import (
    VaccineService,
)

router = APIRouter(
    prefix="/vaccines",
    tags=["Vaccines"],
)


@router.post(
    "",
    response_model=VaccineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vaccine(
    vaccine_data: VaccineCreate,
    db: Session = Depends(get_db),
    service: VaccineService = Depends(
        get_vaccine_service,
    ),
) -> VaccineResponse:
    """Create a new vaccine."""
    return service.create_vaccine(
        db,
        vaccine_data,
    )


@router.get(
    "",
    response_model=list[VaccineResponse],
)
def get_all_vaccines(
    db: Session = Depends(get_db),
    service: VaccineService = Depends(
        get_vaccine_service,
    ),
) -> list[VaccineResponse]:
    """Retrieve all vaccines."""
    return service.get_all_vaccines(
        db,
    )


@router.get(
    "/{vaccine_id}",
    response_model=VaccineResponse,
)
def get_vaccine(
    vaccine_id: int,
    db: Session = Depends(get_db),
    service: VaccineService = Depends(
        get_vaccine_service,
    ),
) -> VaccineResponse:
    """Retrieve a vaccine by ID."""
    return service.get_vaccine(
        db,
        vaccine_id,
    )


@router.put(
    "/{vaccine_id}",
    response_model=VaccineResponse,
)
def update_vaccine(
    vaccine_id: int,
    vaccine_data: VaccineUpdate,
    db: Session = Depends(get_db),
    service: VaccineService = Depends(
        get_vaccine_service,
    ),
) -> VaccineResponse:
    """Update an existing vaccine."""
    return service.update_vaccine(
        db=db,
        vaccine_id=vaccine_id,
        vaccine_data=vaccine_data,
    )


@router.delete(
    "/{vaccine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vaccine(
    vaccine_id: int,
    db: Session = Depends(get_db),
    service: VaccineService = Depends(
        get_vaccine_service,
    ),
) -> Response:
    """Delete a vaccine."""
    service.delete_vaccine(
        db,
        vaccine_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )