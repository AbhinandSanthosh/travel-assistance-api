from src.exceptions.data_collection.document_validation import (
    DocumentValidationNotFoundError,
)
from src.models.data_collection.document_validation import (
    DocumentValidation,
)
from src.repositories.data_collection.document_validation import (
    DocumentValidationRepository,
)
from src.schemas.data_collection.document_validation import (
    DocumentValidationCreate,
    DocumentValidationUpdate,
)
from src.services.base_crud_service import BaseCrudService


class DocumentValidationService:
    """Service for Document Validation."""

    def __init__(
        self,
        repository: DocumentValidationRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(
            repository,
        )

    async def create_document_validation(
        self,
        data: DocumentValidationCreate,
    ) -> DocumentValidation:
        return await self.base_crud.create(data)

    async def get_document_validation(
        self,
        validation_id: int,
    ) -> DocumentValidation:
        validation = await self.base_crud.get_by_id(
            validation_id,
        )

        if validation is None:
            raise DocumentValidationNotFoundError()

        return validation

    async def get_document_validations(
        self,
    ) -> list[DocumentValidation]:
        return await self.base_crud.get_all()

    async def update_document_validation(
        self,
        validation_id: int,
        data: DocumentValidationUpdate,
    ) -> DocumentValidation:
        validation = await self.base_crud.get_by_id(
            validation_id,
        )

        if validation is None:
            raise DocumentValidationNotFoundError()

        return await self.base_crud.update(
            validation,
            data,
        )

    async def delete_document_validation(
        self,
        validation_id: int,
    ) -> None:
        validation = await self.base_crud.get_by_id(
            validation_id,
        )

        if validation is None:
            raise DocumentValidationNotFoundError()

        await self.base_crud.delete(validation)