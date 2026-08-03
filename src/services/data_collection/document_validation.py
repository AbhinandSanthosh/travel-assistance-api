from sqlalchemy.orm import Session

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
        self.base_crud = BaseCrudService(repository)

    def create_document_validation(
        self,
        db: Session,
        data: DocumentValidationCreate,
    ) -> DocumentValidation:
        """Create a document validation."""

        return self.base_crud.create(
            db=db,
            model=DocumentValidation,
            data=data,
        )

    def get_document_validation(
        self,
        db: Session,
        validation_id: int,
    ) -> DocumentValidation:
        """Get document validation by ID."""

        validation = self.base_crud.get_by_id(
            db=db,
            obj_id=validation_id,
        )

        if validation is None:
            raise DocumentValidationNotFoundError(
                validation_id,
            )

        return validation

    def get_document_validations(
        self,
        db: Session,
    ) -> list[DocumentValidation]:
        """Get all document validations."""

        return self.base_crud.get_all(db)

    def update_document_validation(
        self,
        db: Session,
        validation_id: int,
        data: DocumentValidationUpdate,
    ) -> DocumentValidation:
        """Update document validation."""

        validation = self.get_document_validation(
            db=db,
            validation_id=validation_id,
        )

        return self.base_crud.update(
            db=db,
            obj=validation,
            data=data,
        )

    def delete_document_validation(
        self,
        db: Session,
        validation_id: int,
    ) -> None:
        """Delete document validation."""

        validation = self.get_document_validation(
            db=db,
            validation_id=validation_id,
        )

        self.base_crud.delete(
            db=db,
            obj=validation,
        )