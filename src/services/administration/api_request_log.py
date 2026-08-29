from sqlalchemy.orm import Session

from src.exceptions.administration.api_request_log import (
    APIRequestLogNotFoundError,
)
from src.models.administration.api_request_log import (
    APIRequestLog,
)
from src.repositories.administration.api_request_log import (
    APIRequestLogRepository,
)
from src.schemas.administration.api_request_log import (
    APIRequestLogCreate,
)
from src.services.base_crud_service import BaseCrudService


class APIRequestLogService:
    """Service for API Request Logs."""

    def __init__(
        self,
        repository: APIRequestLogRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_api_request_log(
        self,
        db: Session,
        request_log_data: APIRequestLogCreate,
    ) -> APIRequestLog:
        """Create an API request log."""

        return self.base_crud.create(
            db=db,
            model=APIRequestLog,
            data=request_log_data,
        )

    def get_api_request_log(
        self,
        db: Session,
        request_log_id: int,
    ) -> APIRequestLog:
        """Return an API request log by ID."""

        request_log = self.base_crud.get_by_id(
            db=db,
            obj_id=request_log_id,
        )

        if request_log is None:
            raise APIRequestLogNotFoundError(
                request_log_id,
            )

        return request_log

    def get_all_api_request_logs(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[APIRequestLog]:
        """Return all API request logs."""

        return self.base_crud.get_all(db=db, skip=skip, limit=limit)

    def get_api_request_logs_by_client(
        self,
        db: Session,
        client_id: int,
    ) -> list[APIRequestLog]:
        """Return API request logs for an API client."""

        return self.repository.get_by_client_id(
            db=db,
            client_id=client_id,
        )