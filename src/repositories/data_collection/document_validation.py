from src.models.data_collection.document_validation import (
    DocumentValidation,
)
from src.repositories.base_repository import BaseRepository


class DocumentValidationRepository(
    BaseRepository[DocumentValidation]
):
    """Repository for Document Validation."""

    def __init__(self) -> None:
        super().__init__(DocumentValidation)