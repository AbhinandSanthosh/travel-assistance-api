from src.models.data_collection.document_version import (
    DocumentVersion,
)
from src.repositories.base_repository import BaseRepository


class DocumentVersionRepository(
    BaseRepository[DocumentVersion]
):
    """Repository for Document Version."""

    def __init__(self):
        super().__init__(DocumentVersion)

    async def get_by_file_hash(
        self,
        file_hash: str,
    ) -> DocumentVersion | None:
        return await self.get_by_field(
            "file_hash",
            file_hash,
        )

    async def get_by_document_and_version(
        self,
        document_id: int,
        version_number: str,
    ) -> DocumentVersion | None:
        return await self.get_by_fields(
            {
                "document_id": document_id,
                "version_number": version_number,
            }
        )