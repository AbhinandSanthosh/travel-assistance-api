from src.exceptions.data_collection.document_version import (
    DocumentVersionAlreadyExistsError,
    DocumentVersionFileHashAlreadyExistsError,
)
from src.models.data_collection.document_version import (
    DocumentVersion,
)
from src.repositories.data_collection.document_version import (
    DocumentVersionRepository,
)
from src.schemas.data_collection.document_version import (
    DocumentVersionCreate,
    DocumentVersionUpdate,
)
from src.services.base_crud_service import BaseCrudService


class DocumentVersionService:
    """Service for Document Version."""

    def __init__(
        self,
        repository: DocumentVersionRepository,
    ):
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    async def create_document_version(
        self,
        data: DocumentVersionCreate,
    ) -> DocumentVersion:
        version = await self.repository.get_by_document_and_version(
            data.document_id,
            data.version_number,
        )
        if version:
            raise DocumentVersionAlreadyExistsError(
                data.document_id,
                data.version_number,
            )

        file_hash = await self.repository.get_by_file_hash(
            data.file_hash,
        )
        if file_hash:
            raise DocumentVersionFileHashAlreadyExistsError(
                data.file_hash,
            )

        return await self.base_crud.create(data)

    async def get_document_version(
        self,
        document_version_id: int,
    ) -> DocumentVersion:
        return await self.base_crud.get_by_id(document_version_id)

    async def get_document_versions(
        self,
    ) -> list[DocumentVersion]:
        return await self.base_crud.get_all()

    async def update_document_version(
        self,
        document_version_id: int,
        data: DocumentVersionUpdate,
    ) -> DocumentVersion:
        if (
            data.document_id is not None
            and data.version_number is not None
        ):
            version = await self.repository.get_by_document_and_version(
                data.document_id,
                data.version_number,
            )
            if (
                version
                and version.id != document_version_id
            ):
                raise DocumentVersionAlreadyExistsError(
                    data.document_id,
                    data.version_number,
                )

        if data.file_hash:
            file_hash = await self.repository.get_by_file_hash(
                data.file_hash,
            )
            if (
                file_hash
                and file_hash.id != document_version_id
            ):
                raise DocumentVersionFileHashAlreadyExistsError(
                    data.file_hash,
                )

        return await self.base_crud.update(
            document_version_id,
            data,
        )

    async def delete_document_version(
        self,
        document_version_id: int,
    ) -> None:
        await self.base_crud.delete(document_version_id)