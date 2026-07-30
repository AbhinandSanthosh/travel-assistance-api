from src.models.data_collection.ai_extraction import (
    AIExtraction,
)
from src.repositories.base_repository import BaseRepository


class AIExtractionRepository(
    BaseRepository[AIExtraction]
):
    """Repository for AI Extraction."""

    def __init__(self) -> None:
        super().__init__(AIExtraction)