

from sqlalchemy.orm import Session

from src.exceptions.administration.client_usage_statistics import (
    ClientUsageStatisticsAlreadyExistsError,
    ClientUsageStatisticsNotFoundError,
)
from src.models.administration.client_usage_statistics import (
    ClientUsageStatistics,
)
from src.repositories.administration.client_usage_statistics import (
    ClientUsageStatisticsRepository,
)
from src.schemas.administration.client_usage_statistics import (
    ClientUsageStatisticsCreate,
    ClientUsageStatisticsUpdate,
)
from src.services.base_crud_service import BaseCrudService


class ClientUsageStatisticsService:
    """Service for Client Usage Statistics."""

    def __init__(
        self,
        repository: ClientUsageStatisticsRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_client_usage_statistics(
        self,
        db: Session,
        statistics_data: ClientUsageStatisticsCreate,
    ) -> ClientUsageStatistics:
        """Create client usage statistics."""

        existing = self.repository.get_by_client_and_date(
            db=db,
            client_id=statistics_data.client_id,
            usage_date=statistics_data.usage_date,
        )

        if existing:
            raise ClientUsageStatisticsAlreadyExistsError(
                statistics_data.client_id,
                statistics_data.usage_date,
            )

        return self.base_crud.create(
            db=db,
            model=ClientUsageStatistics,
            data=statistics_data,
        )

    def get_client_usage_statistics(
        self,
        db: Session,
        statistics_id: int,
    ) -> ClientUsageStatistics:
        """Return client usage statistics by ID."""

        statistics = self.base_crud.get_by_id(
            db=db,
            obj_id=statistics_id,
        )

        if statistics is None:
            raise ClientUsageStatisticsNotFoundError(
                statistics_id,
            )

        return statistics

    def get_all_client_usage_statistics(
        self,
        db: Session,
    ) -> list[ClientUsageStatistics]:
        """Return all client usage statistics."""

        return self.base_crud.get_all(db=db)

    def get_client_usage_statistics_by_client(
        self,
        db: Session,
        client_id: int,
    ) -> list[ClientUsageStatistics]:
        """Return usage statistics for a client."""

        return self.repository.get_by_client_id(
            db=db,
            client_id=client_id,
        )

    def update_client_usage_statistics(
        self,
        db: Session,
        statistics_id: int,
        statistics_data: ClientUsageStatisticsUpdate,
    ) -> ClientUsageStatistics:
        """Update client usage statistics."""

        statistics = self.get_client_usage_statistics(
            db=db,
            statistics_id=statistics_id,
        )

        return self.base_crud.update(
            db=db,
            obj=statistics,
            data=statistics_data,
        )