from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.data_collection.document_version import (
    DocumentVersion,
)
from src.repositories.base_repository import BaseRepository


class DocumentVersionRepository(
    BaseRepository[DocumentVersion]
):
    """Repository for Document Version."""

    def __init__(self) -> None:
        super().__init__(DocumentVersion)

    def get_by_file_hash(
        self,
        db: Session,
        file_hash: str,
    ) -> DocumentVersion | None:
        return db.scalar(
            select(DocumentVersion).where(
                DocumentVersion.file_hash == file_hash
            )
        )

    def get_by_document_and_version(
        self,
        db: Session,
        document_id: int,
        version_number: str,
    ) -> DocumentVersion | None:
        return db.scalar(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version_number,
            )
        )