from src.exceptions.data_collection.source_registry import (
    SourceRegistryAuthorityNameAlreadyExistsError,
    SourceRegistryWebsiteAlreadyExistsError,
)
from src.models.data_collection.source_registry import SourceRegistry
from src.repositories.data_collection.source_registry import (
    SourceRegistryRepository,
)
from src.schemas.data_collection.source_registry import (
    SourceRegistryCreate,
    SourceRegistryUpdate,
)
from src.services.base_crud_service import BaseCrudService


class SourceRegistryService:
    """Service for Source Registry."""

    def __init__(
        self,
        repository: SourceRegistryRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    async def create_source_registry(
        self,
        data: SourceRegistryCreate,
    ) -> SourceRegistry:
        """Create a source registry."""

        authority = await self.repository.get_by_authority_name(
            data.authority_name,
        )
        if authority:
            raise SourceRegistryAuthorityNameAlreadyExistsError(
                data.authority_name,
            )

        website = await self.repository.get_by_website(
            data.website,
        )
        if website:
            raise SourceRegistryWebsiteAlreadyExistsError(
                data.website,
            )

        return await self.base_crud.create(data)

    async def get_source_registry(
        self,
        registry_id: int,
    ) -> SourceRegistry:
        """Get a source registry by ID."""
        return await self.base_crud.get(registry_id)

    async def get_all_source_registries(
        self,
    ) -> list[SourceRegistry]:
        """Get all source registries."""
        return await self.base_crud.get_all()

    async def update_source_registry(
        self,
        registry_id: int,
        data: SourceRegistryUpdate,
    ) -> SourceRegistry:
        """Update a source registry."""

        existing = await self.base_crud.get(registry_id)

        if (
            data.authority_name
            and data.authority_name != existing.authority_name
        ):
            authority = await self.repository.get_by_authority_name(
                data.authority_name,
            )
            if authority:
                raise SourceRegistryAuthorityNameAlreadyExistsError(
                    data.authority_name,
                )

        if (
            data.website
            and data.website != existing.website
        ):
            website = await self.repository.get_by_website(
                data.website,
            )
            if website:
                raise SourceRegistryWebsiteAlreadyExistsError(
                data.website,
            )

        return await self.base_crud.update(
            registry_id,
            data,
        )

    async def delete_source_registry(
        self,
        registry_id: int,
    ) -> None:
        """Delete a source registry."""
        await self.base_crud.delete(registry_id)