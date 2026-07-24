from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_passport_type_service
from src.db.session import get_db
from src.schemas.reference.passport_type import (
    PassportTypeCreate,
    PassportTypeResponse,
    PassportTypeUpdate,
)
from src.services.reference.passport_type_service import (
    PassportTypeService,
)

router = APIRouter(
    prefix="/passport-types",
    tags=["Passport Types"],
)


@router.post(
    "",
    response_model=PassportTypeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_passport_type(
    passport_type_data: PassportTypeCreate,
    db: Session = Depends(get_db),
    service: PassportTypeService = Depends(
        get_passport_type_service,
    ),
):
    return service.create_passport_type(
        db,
        passport_type_data,
    )


@router.get(
    "",
    response_model=list[PassportTypeResponse],
)
def get_all_passport_types(
    db: Session = Depends(get_db),
    service: PassportTypeService = Depends(
        get_passport_type_service,
    ),
):
    return service.get_all_passport_types(db)


@router.get(
    "/{passport_type_id}",
    response_model=PassportTypeResponse,
)
def get_passport_type(
    passport_type_id: int,
    db: Session = Depends(get_db),
    service: PassportTypeService = Depends(
        get_passport_type_service,
    ),
):
    return service.get_passport_type(
        db,
        passport_type_id,
    )


@router.put(
    "/{passport_type_id}",
    response_model=PassportTypeResponse,
)
def update_passport_type(
    passport_type_id: int,
    passport_type_data: PassportTypeUpdate,
    db: Session = Depends(get_db),
    service: PassportTypeService = Depends(
        get_passport_type_service,
    ),
):
    return service.update_passport_type(
        db,
        passport_type_id,
        passport_type_data,
    )


@router.delete(
    "/{passport_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_passport_type(
    passport_type_id: int,
    db: Session = Depends(get_db),
    service: PassportTypeService = Depends(
        get_passport_type_service,
    ),
):
    service.delete_passport_type(
        db,
        passport_type_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)