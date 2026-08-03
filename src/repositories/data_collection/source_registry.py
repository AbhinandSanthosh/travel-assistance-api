from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.data_collection.source_registry import SourceRegistry
from src.repositories.base_repository import BaseRepository


class SourceRegistryRepository(BaseRepository[SourceRegistry]):
    """Repository for Source Registry."""

    def __init__(self) -> None:
        super().__init__(SourceRegistry)

    def get_by_authority_name(
        self,
        db: Session,
        authority_name: str,
    ) -> SourceRegistry | None:
        return db.scalar(
            select(SourceRegistry).where(
                SourceRegistry.authority_name == authority_name
            )
        )

    def get_by_website(
        self,
        db: Session,
        website: str,
    ) -> SourceRegistry | None:
        return db.scalar(
            select(SourceRegistry).where(
                SourceRegistry.website == website
            )
        )