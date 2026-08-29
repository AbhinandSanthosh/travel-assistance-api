from sqlalchemy.orm import Session

from src.exceptions.data_collection.source_document import (
    SourceDocumentDocumentURLAlreadyExistsError,
    SourceDocumentFileHashAlreadyExistsError,
    SourceDocumentNotFoundError,
)
from src.models.data_collection.source_document import (
    SourceDocument,
)
from src.repositories.data_collection.source_document import (
    SourceDocumentRepository,
)
from src.schemas.data_collection.source_document import (
    SourceDocumentCreate,
    SourceDocumentUpdate,
)
from src.services.base_crud_service import BaseCrudService


class SourceDocumentService:
    """Service for Source Document."""

    def __init__(
        self,
        repository: SourceDocumentRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_source_document(
        self,
        db: Session,
        data: SourceDocumentCreate,
    ) -> SourceDocument:

        document = self.repository.get_by_document_url(
            db,
            data.document_url,
        )

        if document:
            raise SourceDocumentDocumentURLAlreadyExistsError(
                data.document_url,
            )

        file_hash = self.repository.get_by_file_hash(
            db,
            data.file_hash,
        )

        if file_hash:
            raise SourceDocumentFileHashAlreadyExistsError(
                data.file_hash,
            )

        return self.base_crud.create(
            db=db,
            model=SourceDocument,
            data=data,
        )

    def get_source_document(
        self,
        db: Session,
        source_document_id: int,
    ) -> SourceDocument:

        document = self.base_crud.get_by_id(
            db=db,
            obj_id=source_document_id,
        )

        if document is None:
            raise SourceDocumentNotFoundError(
                source_document_id,
            )

        return document

    def get_source_documents(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SourceDocument]:
        return self.base_crud.get_all(db, skip, limit)

    def update_source_document(
        self,
        db: Session,
        source_document_id: int,
        data: SourceDocumentUpdate,
    ) -> SourceDocument:

        document = self.get_source_document(
            db=db,
            source_document_id=source_document_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if (
            "document_url" in update_data
            and update_data["document_url"] != document.document_url
        ):
            existing = self.repository.get_by_document_url(
                db,
                update_data["document_url"],
            )

            if existing:
                raise SourceDocumentDocumentURLAlreadyExistsError(
                    update_data["document_url"],
                )

        if (
            "file_hash" in update_data
            and update_data["file_hash"] != document.file_hash
        ):
            existing = self.repository.get_by_file_hash(
                db,
                update_data["file_hash"],
            )

            if existing:
                raise SourceDocumentFileHashAlreadyExistsError(
                    update_data["file_hash"],
                )

        return self.base_crud.update(
            db=db,
            obj=document,
            data=data,
        )

    def delete_source_document(
        self,
        db: Session,
        source_document_id: int,
    ) -> None:

        document = self.get_source_document(
            db=db,
            source_document_id=source_document_id,
        )

        self.base_crud.delete(
            db=db,
            obj=document,
        )