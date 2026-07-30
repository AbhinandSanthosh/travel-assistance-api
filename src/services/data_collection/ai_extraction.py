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
        self.base_crud = BaseCrudService(
            repository,
        )

    async def create_ai_extraction(
        self,
        data: AIExtractionCreate,
    ) -> AIExtraction:
        return await self.base_crud.create(data)

    async def get_ai_extraction(
        self,
        extraction_id: int,
    ) -> AIExtraction:
        extraction = await self.base_crud.get_by_id(
            extraction_id,
        )

        if extraction is None:
            raise AIExtractionNotFoundError()

        return extraction

    async def get_ai_extractions(
        self,
    ) -> list[AIExtraction]:
        return await self.base_crud.get_all()

    async def update_ai_extraction(
        self,
        extraction_id: int,
        data: AIExtractionUpdate,
    ) -> AIExtraction:
        extraction = await self.base_crud.get_by_id(
            extraction_id,
        )

        if extraction is None:
            raise AIExtractionNotFoundError()

        return await self.base_crud.update(
            extraction,
            data,
        )

    async def delete_ai_extraction(
        self,
        extraction_id: int,
    ) -> None:
        extraction = await self.base_crud.get_by_id(
            extraction_id,
        )

        if extraction is None:
            raise AIExtractionNotFoundError()

        await self.base_crud.delete(extraction)