from src.exceptions.data_collection.source_document import (
    SourceDocumentDocumentURLAlreadyExistsError,
    SourceDocumentFileHashAlreadyExistsError,
)
from src.models.data_collection.source_document import SourceDocument
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
    ):
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    async def create_source_document(
        self,
        data: SourceDocumentCreate,
    ) -> SourceDocument:
        document = await self.repository.get_by_document_url(
            data.document_url,
        )
        if document:
            raise SourceDocumentDocumentURLAlreadyExistsError(
                data.document_url,
            )

        file_hash = await self.repository.get_by_file_hash(
            data.file_hash,
        )
        if file_hash:
            raise SourceDocumentFileHashAlreadyExistsError(
                data.file_hash,
            )

        return await self.base_crud.create(data)

    async def get_source_document(
        self,
        source_document_id: int,
    ) -> SourceDocument:
        return await self.base_crud.get_by_id(source_document_id)

    async def get_source_documents(
        self,
    ) -> list[SourceDocument]:
        return await self.base_crud.get_all()

    async def update_source_document(
        self,
        source_document_id: int,
        data: SourceDocumentUpdate,
    ) -> SourceDocument:
        if data.document_url:
            document = await self.repository.get_by_document_url(
                data.document_url,
            )
            if (
                document
                and document.id != source_document_id
            ):
                raise SourceDocumentDocumentURLAlreadyExistsError(
                    data.document_url,
                )

        if data.file_hash:
            file_hash = await self.repository.get_by_file_hash(
                data.file_hash,
            )
            if (
                file_hash
                and file_hash.id != source_document_id
            ):
                raise SourceDocumentFileHashAlreadyExistsError(
                    data.file_hash,
                )

        return await self.base_crud.update(
            source_document_id,
            data,
        )

    async def delete_source_document(
        self,
        source_document_id: int,
    ) -> None:
        await self.base_crud.delete(source_document_id)