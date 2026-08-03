from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_source_document_service,
)
from src.db.session import get_db
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
def create_source_document(
    data: SourceDocumentCreate,
    db: Session = Depends(get_db),
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Create a source document."""

    return service.create_source_document(
        db=db,
        data=data,
    )


@router.get(
    "/",
    response_model=list[SourceDocumentResponse],
)
def get_source_documents(
    db: Session = Depends(get_db),
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> list[SourceDocument]:
    """Get all source documents."""

    return service.get_source_documents(
        db=db,
    )


@router.get(
    "/{source_document_id}",
    response_model=SourceDocumentResponse,
)
def get_source_document(
    source_document_id: int,
    db: Session = Depends(get_db),
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Get a source document by ID."""

    return service.get_source_document(
        db=db,
        source_document_id=source_document_id,
    )


@router.put(
    "/{source_document_id}",
    response_model=SourceDocumentResponse,
)
def update_source_document(
    source_document_id: int,
    data: SourceDocumentUpdate,
    db: Session = Depends(get_db),
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> SourceDocument:
    """Update a source document."""

    return service.update_source_document(
        db=db,
        source_document_id=source_document_id,
        data=data,
    )


@router.delete(
    "/{source_document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_source_document(
    source_document_id: int,
    db: Session = Depends(get_db),
    service: SourceDocumentService = Depends(
        get_source_document_service,
    ),
) -> None:
    """Delete a source document."""

    service.delete_source_document(
        db=db,
        source_document_id=source_document_id,
    )