from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.data_collection.source_document import (
    SourceDocument,
)
from src.repositories.base_repository import BaseRepository


class SourceDocumentRepository(
    BaseRepository[SourceDocument]
):
    """Repository for Source Document."""

    def __init__(self) -> None:
        super().__init__(SourceDocument)

    def get_by_document_url(
        self,
        db: Session,
        document_url: str,
    ) -> SourceDocument | None:
        return db.scalar(
            select(SourceDocument).where(
                SourceDocument.document_url == document_url
            )
        )

    def get_by_file_hash(
        self,
        db: Session,
        file_hash: str,
    ) -> SourceDocument | None:
        return db.scalar(
            select(SourceDocument).where(
                SourceDocument.file_hash == file_hash
            )
        )