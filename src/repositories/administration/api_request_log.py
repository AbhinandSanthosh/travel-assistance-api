from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.api_request_log import (
    APIRequestLog,
)
from src.repositories.base_repository import BaseRepository


class APIRequestLogRepository(
    BaseRepository[APIRequestLog]
):
    """Repository for API Request Logs."""

    def __init__(self) -> None:
        super().__init__(APIRequestLog)

    def get_by_client_id(
        self,
        db: Session,
        client_id: int,
    ) -> list[APIRequestLog]:
        """Return API request logs for an API client."""

        return list(
            db.scalars(
                select(APIRequestLog).where(
                    APIRequestLog.client_id == client_id,
                )
            ).all()
        )