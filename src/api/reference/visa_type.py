from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_visa_type_service
from src.db.session import get_db
from src.schemas.reference.visa_type import (
    VisaTypeCreate,
    VisaTypeResponse,
    VisaTypeUpdate,
)
from src.services.reference.visa_type import (
    VisaTypeService,
)

router = APIRouter(
    prefix="/visa-types",
    tags=["Visa Types"],
)


@router.post(
    "",
    response_model=VisaTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visa_type(
    visa_type_data: VisaTypeCreate,
    db: Session = Depends(get_db),
    service: VisaTypeService = Depends(
        get_visa_type_service,
    ),
):
    return service.create_visa_type(
        db,
        visa_type_data,
    )


@router.get(
    "",
    response_model=list[VisaTypeResponse],
)
def get_all_visa_types(
    db: Session = Depends(get_db),
    service: VisaTypeService = Depends(
        get_visa_type_service,
    ),
):
    return service.get_all_visa_types(db)


@router.get(
    "/{visa_type_id}",
    response_model=VisaTypeResponse,
)
def get_visa_type(
    visa_type_id: int,
    db: Session = Depends(get_db),
    service: VisaTypeService = Depends(
        get_visa_type_service,
    ),
):
    return service.get_visa_type(
        db,
        visa_type_id,
    )


@router.put(
    "/{visa_type_id}",
    response_model=VisaTypeResponse,
)
def update_visa_type(
    visa_type_id: int,
    visa_type_data: VisaTypeUpdate,
    db: Session = Depends(get_db),
    service: VisaTypeService = Depends(
        get_visa_type_service,
    ),
):
    return service.update_visa_type(
        db,
        visa_type_id,
        visa_type_data,
    )


@router.delete(
    "/{visa_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_visa_type(
    visa_type_id: int,
    db: Session = Depends(get_db),
    service: VisaTypeService = Depends(
        get_visa_type_service,
    ),
):
    service.delete_visa_type(
        db,
        visa_type_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )