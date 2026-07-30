from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_api_request_log_service,
)
from src.db.session import get_db
from src.schemas.administration.api_request_log import (
    APIRequestLogCreate,
    APIRequestLogResponse,
)
from src.services.administration.api_request_log import (
    APIRequestLogService,
)

router = APIRouter(
    prefix="/api-request-logs",
    tags=["API Request Logs"],
)


@router.post(
    "",
    response_model=APIRequestLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_api_request_log(
    request_log_data: APIRequestLogCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIRequestLogService,
        Depends(get_api_request_log_service),
    ],
) -> APIRequestLogResponse:
    """Create an API request log."""

    return service.create_api_request_log(
        db=db,
        request_log_data=request_log_data,
    )


@router.get(
    "",
    response_model=list[APIRequestLogResponse],
)
def get_all_api_request_logs(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIRequestLogService,
        Depends(get_api_request_log_service),
    ],
) -> list[APIRequestLogResponse]:
    """Return all API request logs."""

    return service.get_all_api_request_logs(db)


@router.get(
    "/{request_log_id}",
    response_model=APIRequestLogResponse,
)
def get_api_request_log(
    request_log_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIRequestLogService,
        Depends(get_api_request_log_service),
    ],
) -> APIRequestLogResponse:
    """Return an API request log by ID."""

    return service.get_api_request_log(
        db=db,
        request_log_id=request_log_id,
    )


@router.get(
    "/client/{client_id}",
    response_model=list[APIRequestLogResponse],
)
def get_api_request_logs_by_client(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIRequestLogService,
        Depends(get_api_request_log_service),
    ],
) -> list[APIRequestLogResponse]:
    """Return API request logs for an API client."""

    return service.get_api_request_logs_by_client(
        db=db,
        client_id=client_id,
    )