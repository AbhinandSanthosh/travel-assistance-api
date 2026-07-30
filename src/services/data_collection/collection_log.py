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
    ):
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    async def create_collection_log(
        self,
        data: CollectionLogCreate,
    ) -> CollectionLog:
        return await self.base_crud.create(data)

    async def get_collection_log(
        self,
        collection_log_id: int,
    ) -> CollectionLog:
        return await self.base_crud.get_by_id(
            collection_log_id,
        )

    async def get_collection_logs(
        self,
    ) -> list[CollectionLog]:
        return await self.base_crud.get_all()

    async def update_collection_log(
        self,
        collection_log_id: int,
        data: CollectionLogUpdate,
    ) -> CollectionLog:
        return await self.base_crud.update(
            collection_log_id,
            data,
        )

    async def delete_collection_log(
        self,
        collection_log_id: int,
    ) -> None:
        await self.base_crud.delete(
            collection_log_id,
        )