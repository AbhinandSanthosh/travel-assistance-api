from fastapi import APIRouter, Depends, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.data_collection import (
    get_collection_log_service,
)
from src.db.session import get_db
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
    dependencies=[Depends(require_permission("data_collection.write"))],
    response_model=CollectionLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection_log(
    data: CollectionLogCreate,
    db: Session = Depends(get_db),
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:

    return service.create_collection_log(
        db=db,
        data=data,
    )


@router.get(
    "/",
    response_model=list[CollectionLogResponse],
)
def get_collection_logs(
    db: Session = Depends(get_db),
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> list[CollectionLog]:

    return service.get_collection_logs(
        db=db,
    )


@router.get(
    "/{collection_log_id}",
    response_model=CollectionLogResponse,
)
def get_collection_log(
    collection_log_id: int,
    db: Session = Depends(get_db),
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:

    return service.get_collection_log(
        db=db,
        collection_log_id=collection_log_id,
    )


@router.put(
    "/{collection_log_id}",
    dependencies=[Depends(require_permission("data_collection.write"))],
    response_model=CollectionLogResponse,
)
def update_collection_log(
    collection_log_id: int,
    data: CollectionLogUpdate,
    db: Session = Depends(get_db),
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> CollectionLog:

    return service.update_collection_log(
        db=db,
        collection_log_id=collection_log_id,
        data=data,
    )


@router.delete(
    "/{collection_log_id}",
    dependencies=[Depends(require_permission("data_collection.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_collection_log(
    collection_log_id: int,
    db: Session = Depends(get_db),
    service: CollectionLogService = Depends(
        get_collection_log_service,
    ),
) -> None:

    service.delete_collection_log(
        db=db,
        collection_log_id=collection_log_id,
    )