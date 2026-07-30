from fastapi import APIRouter, Depends, status

from src.api.dependencies.data_collection import (
    get_collection_log_service,
)
from src.models.data_collection.collection_log import (
    CollectionLog,
)
from src.schemas.data_collection.collection_log import (
    CollectionLogCreate,
    CollectionLogResponse,
    CollectionLogUpdate,
)
from src.services.data_collection.collection_log import (
    CollectionLogService,
)

router = APIRouter(
    prefix="/collection-logs",
    tags=["Collection Logs"],
)


@router.post(
    "/",
    response_model=CollectionLogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_collection_log(
    data: CollectionLogCreate,
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:
    return await service.create_collection_log(data)


@router.get(
    "/",
    response_model=list[CollectionLogResponse],
)
async def get_collection_logs(
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> list[CollectionLog]:
    return await service.get_collection_logs()


@router.get(
    "/{collection_log_id}",
    response_model=CollectionLogResponse,
)
async def get_collection_log(
    collection_log_id: int,
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:
    return await service.get_collection_log(
        collection_log_id,
    )


@router.put(
    "/{collection_log_id}",
    response_model=CollectionLogResponse,
)
async def update_collection_log(
    collection_log_id: int,
    data: CollectionLogUpdate,
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:
    return await service.update_collection_log(
        collection_log_id,
        data,
    )


@router.delete(
    "/{collection_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_collection_log(
    collection_log_id: int,
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> None:
    await service.delete_collection_log(
        collection_log_id,
    )