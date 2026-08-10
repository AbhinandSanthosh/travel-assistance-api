from fastapi import APIRouter, Depends, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_document_version_service,
)
from src.db.session import get_db
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
    dependencies=[Depends(require_permission("data_collection.write"))],
    response_model=DocumentVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document_version(
    data: DocumentVersionCreate,
    db: Session = Depends(get_db),
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:

    return service.create_document_version(
        db=db,
        data=data,
    )


@router.get(
    "/",
    response_model=list[DocumentVersionResponse],
)
def get_document_versions(
    db: Session = Depends(get_db),
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> list[DocumentVersion]:

    return service.get_document_versions(
        db=db,
    )


@router.get(
    "/{document_version_id}",
    response_model=DocumentVersionResponse,
)
def get_document_version(
    document_version_id: int,
    db: Session = Depends(get_db),
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:

    return service.get_document_version(
        db=db,
        document_version_id=document_version_id,
    )


@router.put(
    "/{document_version_id}",
    dependencies=[Depends(require_permission("data_collection.write"))],
    response_model=DocumentVersionResponse,
)
def update_document_version(
    document_version_id: int,
    data: DocumentVersionUpdate,
    db: Session = Depends(get_db),
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> DocumentVersion:

    return service.update_document_version(
        db=db,
        document_version_id=document_version_id,
        data=data,
    )


@router.delete(
    "/{document_version_id}",
    dependencies=[Depends(require_permission("data_collection.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document_version(
    document_version_id: int,
    db: Session = Depends(get_db),
    service: DocumentVersionService = Depends(
        get_document_version_service,
    ),
) -> None:

    service.delete_document_version(
        db=db,
        document_version_id=document_version_id,
    )