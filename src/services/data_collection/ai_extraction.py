from sqlalchemy.orm import Session

from src.exceptions.data_collection.ai_extraction import (
    AIExtractionNotFoundError,
)
from src.models.data_collection.ai_extraction import (
    AIExtraction,
)
from src.repositories.data_collection.ai_extraction import (
    AIExtractionRepository,
)
from src.schemas.data_collection.ai_extraction import (
    AIExtractionCreate,
    AIExtractionUpdate,
)
from src.services.base_crud_service import BaseCrudService


class AIExtractionService:
    """Service for AI Extraction."""

    def __init__(
        self,
        repository: AIExtractionRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_ai_extraction(
        self,
        db: Session,
        data: AIExtractionCreate,
    ) -> AIExtraction:
        """Create AI extraction."""

        return self.base_crud.create(
            db=db,
            model=AIExtraction,
            data=data,
        )

    def get_ai_extraction(
        self,
        db: Session,
        extraction_id: int,
    ) -> AIExtraction:
        """Get AI extraction by ID."""

        extraction = self.base_crud.get_by_id(
            db=db,
            obj_id=extraction_id,
        )

        if extraction is None:
            raise AIExtractionNotFoundError(
                extraction_id,
            )

        return extraction

    def get_ai_extractions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AIExtraction]:
        """Get all AI extractions."""


        return self.base_crud.get_all(db, skip, limit)

    def update_ai_extraction(
        self,
        db: Session,
        extraction_id: int,
        data: AIExtractionUpdate,
    ) -> AIExtraction:
        """Update AI extraction."""

        extraction = self.get_ai_extraction(
            db=db,
            extraction_id=extraction_id,
        )

        return self.base_crud.update(
            db=db,
            obj=extraction,
            data=data,
        )

    def delete_ai_extraction(
        self,
        db: Session,
        extraction_id: int,
    ) -> None:
        """Delete AI extraction."""

        extraction = self.get_ai_extraction(
            db=db,
            extraction_id=extraction_id,
        )

        self.base_crud.delete(
            db=db,
            obj=extraction,
        )