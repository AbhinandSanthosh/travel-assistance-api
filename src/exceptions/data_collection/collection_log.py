from src.exceptions.base import AppException


class CollectionLogNotFoundError(AppException):
    """Raised when a collection log is not found."""

    def __init__(self, collection_log_id: int):
        super().__init__(
            f"Collection log with id {collection_log_id} was not found."
        )