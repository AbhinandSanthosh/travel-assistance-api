from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.client_usage_statistics import (
    ClientUsageStatistics,
)
from src.repositories.base_repository import BaseRepository


class ClientUsageStatisticsRepository(
    BaseRepository[ClientUsageStatistics]
):
    """Repository for Client Usage Statistics."""

    def __init__(self) -> None:
        super().__init__(ClientUsageStatistics)

    def get_by_client_id(
        self,
        db: Session,
        client_id: int,
    ) -> list[ClientUsageStatistics]:
        """Return usage statistics for a client."""

        return list(
            db.scalars(
                select(ClientUsageStatistics).where(
                    ClientUsageStatistics.client_id == client_id,
                )
            ).all()
        )

    def get_by_client_and_date(
        self,
        db: Session,
        client_id: int,
        usage_date: date,
    ) -> ClientUsageStatistics | None:
        """Return usage statistics for a client on a specific date."""

        return db.scalar(
            select(ClientUsageStatistics).where(
                ClientUsageStatistics.client_id == client_id,
                ClientUsageStatistics.usage_date == usage_date,
            )
        )