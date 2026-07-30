from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_document_version_service,
)
from src.models.data_collection.document_version import (
    DocumentVersion,
)
from src.schemas.data_collection.document_version import (
    DocumentVersionCreate,
    DocumentVersionResponse,
    DocumentVersionUpdate,
)
from src.services.data_collection.document_version import (
    DocumentVersionService,
)

router = APIRouter(
    prefix="/document-versions",
    tags=["Document Versions"],
)


@router.post(
    "/",
    response_model=DocumentVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_version(
    data: DocumentVersionCreate,
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:
    return await service.create_document_version(data)


@router.get(
    "/",
    response_model=list[DocumentVersionResponse],
)
async def get_document_versions(
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> list[DocumentVersion]:
    return await service.get_document_versions()


@router.get(
    "/{document_version_id}",
    response_model=DocumentVersionResponse,
)
async def get_document_version(
    document_version_id: int,
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:
    return await service.get_document_version(
        document_version_id,
    )


@router.put(
    "/{document_version_id}",
    response_model=DocumentVersionResponse,
)
async def update_document_version(
    document_version_id: int,
    data: DocumentVersionUpdate,
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:
    return await service.update_document_version(
        document_version_id,
        data,
    )


@router.delete(
    "/{document_version_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_version(
    document_version_id: int,
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> None:
    await service.delete_document_version(
        document_version_id,
    )