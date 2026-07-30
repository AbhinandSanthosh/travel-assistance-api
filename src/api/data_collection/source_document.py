from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_source_document_service,
)
from src.models.data_collection.source_document import (
    SourceDocument,
)
from src.schemas.data_collection.source_document import (
    SourceDocumentCreate,
    SourceDocumentResponse,
    SourceDocumentUpdate,
)
from src.services.data_collection.source_document import (
    SourceDocumentService,
)

router = APIRouter(
    prefix="/source-documents",
    tags=["Source Documents"],
)


@router.post(
    "/",
    response_model=SourceDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_source_document(
    data: SourceDocumentCreate,
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Create a source document."""
    return await service.create_source_document(data)


@router.get(
    "/",
    response_model=list[SourceDocumentResponse],
)
async def get_source_documents(
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> list[SourceDocument]:
    """Get all source documents."""
    return await service.get_source_documents()


@router.get(
    "/{source_document_id}",
    response_model=SourceDocumentResponse,
)
async def get_source_document(
    source_document_id: int,
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Get a source document by ID."""
    return await service.get_source_document(
        source_document_id,
    )


@router.put(
    "/{source_document_id}",
    response_model=SourceDocumentResponse,
)
async def update_source_document(
    source_document_id: int,
    data: SourceDocumentUpdate,
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Update a source document."""
    return await service.update_source_document(
        source_document_id,
        data,
    )


@router.delete(
    "/{source_document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_source_document(
    source_document_id: int,
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> None:
    """Delete a source document."""
    await service.delete_source_document(
        source_document_id,
    )