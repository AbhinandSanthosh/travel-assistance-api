from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_document_validation_service,
)
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
async def create_document_validation(
    data: DocumentValidationCreate,
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:
    return await service.create_document_validation(data)


@router.get(
    "/",
    response_model=list[DocumentValidationResponse],
)
async def get_document_validations(
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> list[DocumentValidation]:
    return await service.get_document_validations()


@router.get(
    "/{validation_id}",
    response_model=DocumentValidationResponse,
)
async def get_document_validation(
    validation_id: int,
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:
    return await service.get_document_validation(
        validation_id,
    )


@router.put(
    "/{validation_id}",
    response_model=DocumentValidationResponse,
)
async def update_document_validation(
    validation_id: int,
    data: DocumentValidationUpdate,
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> DocumentValidation:
    return await service.update_document_validation(
        validation_id,
        data,
    )


@router.delete(
    "/{validation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_validation(
    validation_id: int,
    service: DocumentValidationService = Depends(
        get_document_validation_service,
    ),
) -> None:
    await service.delete_document_validation(
        validation_id,
    )