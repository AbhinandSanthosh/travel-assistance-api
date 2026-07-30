from src.models.data_collection.source_registry import SourceRegistry
from src.repositories.base_repository import BaseRepository


class SourceRegistryRepository(BaseRepository[SourceRegistry]):
    """Repository for Source Registry."""

    def __init__(self) -> None:
        super().__init__(SourceRegistry)

    async def get_by_authority_name(
        self,
        authority_name: str,
    ) -> SourceRegistry | None:
        """Get a source registry by authority name."""
        return await self.find_one_by(
            authority_name=authority_name,
        )

    async def get_by_website(
        self,
        website: str,
    ) -> SourceRegistry | None:
        """Get a source registry by website."""
        return await self.find_one_by(
            website=website,
        )