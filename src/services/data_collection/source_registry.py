from sqlalchemy.orm import Session

from src.exceptions.data_collection.source_registry import (
    SourceRegistryAuthorityNameAlreadyExistsError,
    SourceRegistryNotFoundError,
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

    def create_source_registry(
        self,
        db: Session,
        data: SourceRegistryCreate,
    ) -> SourceRegistry:
        """Create a source registry."""

        authority = self.repository.get_by_authority_name(
            db,
            data.authority_name,
        )

        if authority:
            raise SourceRegistryAuthorityNameAlreadyExistsError(
                data.authority_name,
            )

        website = self.repository.get_by_website(
            db,
            data.website,
        )

        if website:
            raise SourceRegistryWebsiteAlreadyExistsError(
                data.website,
            )

        return self.base_crud.create(
            db=db,
            model=SourceRegistry,
            data=data,
        )

    def get_source_registry(
        self,
        db: Session,
        registry_id: int,
    ) -> SourceRegistry:
        """Get a source registry by ID."""

        registry = self.base_crud.get_by_id(
            db=db,
            obj_id=registry_id,
        )

        if registry is None:
            raise SourceRegistryNotFoundError(
                registry_id,
            )

        return registry

    def get_all_source_registries(
        self,
        db: Session,
    ) -> list[SourceRegistry]:
        """Get all source registries."""

        return self.base_crud.get_all(db)

    def update_source_registry(
        self,
        db: Session,
        registry_id: int,
        data: SourceRegistryUpdate,
    ) -> SourceRegistry:
        """Update a source registry."""

        registry = self.get_source_registry(
            db=db,
            registry_id=registry_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if (
            "authority_name" in update_data
            and update_data["authority_name"] != registry.authority_name
        ):
            authority = self.repository.get_by_authority_name(
                db,
                update_data["authority_name"],
            )

            if authority:
                raise SourceRegistryAuthorityNameAlreadyExistsError(
                    update_data["authority_name"],
                )

        if (
            "website" in update_data
            and update_data["website"] != registry.website
        ):
            website = self.repository.get_by_website(
                db,
                update_data["website"],
            )

            if website:
                raise SourceRegistryWebsiteAlreadyExistsError(
                    update_data["website"],
                )

        return self.base_crud.update(
            db=db,
            obj=registry,
            data=data,
        )

    def delete_source_registry(
        self,
        db: Session,
        registry_id: int,
    ) -> None:
        """Delete a source registry."""

        registry = self.get_source_registry(
            db=db,
            registry_id=registry_id,
        )

        self.base_crud.delete(
            db=db,
            obj=registry,
        )