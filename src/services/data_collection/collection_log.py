from sqlalchemy.orm import Session

from src.exceptions.data_collection.collection_log import (
    CollectionLogNotFoundError,
)
from src.models.data_collection.collection_log import (
    CollectionLog,
)
from src.repositories.data_collection.collection_log import (
    CollectionLogRepository,
)
from src.schemas.data_collection.collection_log import (
    CollectionLogCreate,
    CollectionLogUpdate,
)
from src.services.base_crud_service import BaseCrudService


class CollectionLogService:
    """Service for Collection Log."""

    def __init__(
        self,
        repository: CollectionLogRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_collection_log(
        self,
        db: Session,
        data: CollectionLogCreate,
    ) -> CollectionLog:

        return self.base_crud.create(
            db=db,
            model=CollectionLog,
            data=data,
        )

    def get_collection_log(
        self,
        db: Session,
        collection_log_id: int,
    ) -> CollectionLog:

        log = self.base_crud.get_by_id(
            db=db,
            obj_id=collection_log_id,
        )

        if log is None:
            raise CollectionLogNotFoundError(
                collection_log_id,
            )

        return log

    def get_collection_logs(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CollectionLog]:
        return self.base_crud.get_all(db, skip, limit)

    def update_collection_log(
        self,
        db: Session,
        collection_log_id: int,
        data: CollectionLogUpdate,
    ) -> CollectionLog:

        log = self.get_collection_log(
            db=db,
            collection_log_id=collection_log_id,
        )

        return self.base_crud.update(
            db=db,
            obj=log,
            data=data,
        )

    def delete_collection_log(
        self,
        db: Session,
        collection_log_id: int,
    ) -> None:

        log = self.get_collection_log(
            db=db,
            collection_log_id=collection_log_id,
        )

        self.base_crud.delete(
            db=db,
            obj=log,
        )