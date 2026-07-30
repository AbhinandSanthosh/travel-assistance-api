from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_source_registry_service,
)
from src.models.data_collection.source_registry import SourceRegistry
from src.schemas.data_collection.source_registry import (
    SourceRegistryCreate,
    SourceRegistryResponse,
    SourceRegistryUpdate,
)
from src.services.data_collection.source_registry import (
    SourceRegistryService,
)

router = APIRouter(prefix="/source-registries", tags=["Source Registry"])


@router.post(
    "",
    response_model=SourceRegistryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_source_registry(
    data: SourceRegistryCreate,
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Create a source registry."""
    return await service.create_source_registry(data)


@router.get(
    "",
    response_model=list[SourceRegistryResponse],
)
async def get_source_registries(
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> list[SourceRegistry]:
    """Get all source registries."""
    return await service.get_all_source_registries()


@router.get(
    "/{registry_id}",
    response_model=SourceRegistryResponse,
)
async def get_source_registry(
    registry_id: int,
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Get a source registry by ID."""
    return await service.get_source_registry(registry_id)


@router.put(
    "/{registry_id}",
    response_model=SourceRegistryResponse,
)
async def update_source_registry(
    registry_id: int,
    data: SourceRegistryUpdate,
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> SourceRegistry:
    """Update a source registry."""
    return await service.update_source_registry(
        registry_id,
        data,
    )


@router.delete(
    "/{registry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_source_registry(
    registry_id: int,
    service: SourceRegistryService = Depends(
        get_source_registry_service,
    ),
) -> None:
    """Delete a source registry."""
    await service.delete_source_registry(registry_id)