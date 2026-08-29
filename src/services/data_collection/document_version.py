from sqlalchemy.orm import Session

from src.exceptions.data_collection.document_version import (
    DocumentVersionAlreadyExistsError,
    DocumentVersionFileHashAlreadyExistsError,
    DocumentVersionNotFoundError,
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
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_document_version(
        self,
        db: Session,
        data: DocumentVersionCreate,
    ) -> DocumentVersion:

        version = self.repository.get_by_document_and_version(
            db,
            data.document_id,
            data.version_number,
        )

        if version:
            raise DocumentVersionAlreadyExistsError(
                data.document_id,
                data.version_number,
            )

        file_hash = self.repository.get_by_file_hash(
            db,
            data.file_hash,
        )

        if file_hash:
            raise DocumentVersionFileHashAlreadyExistsError(
                data.file_hash,
            )

        return self.base_crud.create(
            db=db,
            model=DocumentVersion,
            data=data,
        )

    def get_document_version(
        self,
        db: Session,
        document_version_id: int,
    ) -> DocumentVersion:

        version = self.base_crud.get_by_id(
            db=db,
            obj_id=document_version_id,
        )

        if version is None:
            raise DocumentVersionNotFoundError(
                document_version_id,
            )

        return version

    def get_document_versions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[DocumentVersion]:
        return self.base_crud.get_all(db, skip, limit)

    def update_document_version(
        self,
        db: Session,
        document_version_id: int,
        data: DocumentVersionUpdate,
    ) -> DocumentVersion:

        version = self.get_document_version(
            db=db,
            document_version_id=document_version_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if (
            "document_id" in update_data
            and "version_number" in update_data
        ):
            existing = self.repository.get_by_document_and_version(
                db,
                update_data["document_id"],
                update_data["version_number"],
            )

            if (
                existing
                and existing.id != document_version_id
            ):
                raise DocumentVersionAlreadyExistsError(
                    update_data["document_id"],
                    update_data["version_number"],
                )

        if (
            "file_hash" in update_data
            and update_data["file_hash"] != version.file_hash
        ):
            existing = self.repository.get_by_file_hash(
                db,
                update_data["file_hash"],
            )

            if existing:
                raise DocumentVersionFileHashAlreadyExistsError(
                    update_data["file_hash"],
                )

        return self.base_crud.update(
            db=db,
            obj=version,
            data=data,
        )

    def delete_document_version(
        self,
        db: Session,
        document_version_id: int,
    ) -> None:

        version = self.get_document_version(
            db=db,
            document_version_id=document_version_id,
        )

        self.base_crud.delete(
            db=db,
            obj=version,
        )