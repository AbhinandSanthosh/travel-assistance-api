from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_document_validation_service,
)
from src.db.session import get_db
from src.models.data_collection.document_validation import (
    DocumentValidation,
)
from src.schemas.data_collection.document_validation import (
    DocumentValidationCreate,
    DocumentValidationResponse,
    DocumentValidationUpdate,
)
from src.services.data_collection.document_validation import (
    DocumentValidationService,
)

router = APIRouter(
    prefix="/document-validations",
    tags=["Document Validations"],
)


@router.post(
    "/",
    response_model=DocumentValidationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document_validation(
    data: DocumentValidationCreate,
    db: Session = Depends(get_db),
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:

    return service.create_document_validation(
        db=db,
        data=data,
    )


@router.get(
    "/",
    response_model=list[DocumentValidationResponse],
)
def get_document_validations(
    db: Session = Depends(get_db),
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> list[DocumentValidation]:

    return service.get_document_validations(
        db=db,
    )


@router.get(
    "/{validation_id}",
    response_model=DocumentValidationResponse,
)
def get_document_validation(
    validation_id: int,
    db: Session = Depends(get_db),
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:

    return service.get_document_validation(
        db=db,
        validation_id=validation_id,
    )


@router.put(
    "/{validation_id}",
    response_model=DocumentValidationResponse,
)
def update_document_validation(
    validation_id: int,
    data: DocumentValidationUpdate,
    db: Session = Depends(get_db),
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:

    return service.update_document_validation(
        db=db,
        validation_id=validation_id,
        data=data,
    )


@router.delete(
    "/{validation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document_validation(
    validation_id: int,
    db: Session = Depends(get_db),
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> None:

    service.delete_document_validation(
        db=db,
        validation_id=validation_id,
    )