from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_source_registry_service,
)
from src.db.session import get_db
from src.models.data_collection.source_registry import SourceRegistry
from src.schemas.data_collection.source_registry import (
    SourceRegistryCreate,
    SourceRegistryResponse,
    SourceRegistryUpdate,
)
from src.services.data_collection.source_registry import (
    SourceRegistryService,
)

router = APIRouter(
    prefix="/source-registries",
    tags=["Source Registry"],
)


@router.post(
    "",
    response_model=SourceRegistryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_source_registry(
    data: SourceRegistryCreate,
    db: Session = Depends(get_db),
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Create a source registry."""

    return service.create_source_registry(
        db=db,
        data=data,
    )


@router.get(
    "",
    response_model=list[SourceRegistryResponse],
)
def get_source_registries(
    db: Session = Depends(get_db),
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> list[SourceRegistry]:
    """Get all source registries."""

    return service.get_all_source_registries(
        db=db,
    )


@router.get(
    "/{registry_id}",
    response_model=SourceRegistryResponse,
)
def get_source_registry(
    registry_id: int,
    db: Session = Depends(get_db),
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Get a source registry by ID."""

    return service.get_source_registry(
        db=db,
        registry_id=registry_id,
    )


@router.put(
    "/{registry_id}",
    response_model=SourceRegistryResponse,
)
def update_source_registry(
    registry_id: int,
    data: SourceRegistryUpdate,
    db: Session = Depends(get_db),
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Update a source registry."""

    return service.update_source_registry(
        db=db,
        registry_id=registry_id,
        data=data,
    )


@router.delete(
    "/{registry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_source_registry(
    registry_id: int,
    db: Session = Depends(get_db),
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> None:
    """Delete a source registry."""

    service.delete_source_registry(
        db=db,
        registry_id=registry_id,
    )