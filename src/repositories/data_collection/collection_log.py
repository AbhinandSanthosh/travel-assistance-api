from src.models.data_collection.collection_log import (
    CollectionLog,
)
from src.repositories.base_repository import BaseRepository


class CollectionLogRepository(
    BaseRepository[CollectionLog]
):
    """Repository for Collection Log."""

    def __init__(self):
        super().__init__(CollectionLog)