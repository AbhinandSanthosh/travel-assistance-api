from src.models.data_collection.source_document import (
    SourceDocument,
)
from src.repositories.base_repository import BaseRepository


class SourceDocumentRepository(
    BaseRepository[SourceDocument]
):
    """Repository for Source Document."""

    def __init__(self):
        super().__init__(SourceDocument)

    async def get_by_document_url(
        self,
        document_url: str,
    ) -> SourceDocument | None:
        return await self.get_by_field(
            "document_url",
            document_url,
        )

    async def get_by_file_hash(
        self,
        file_hash: str,
    ) -> SourceDocument | None:
        return await self.get_by_field(
            "file_hash",
            file_hash,
        )