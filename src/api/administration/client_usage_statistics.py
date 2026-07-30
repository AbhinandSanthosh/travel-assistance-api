from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_client_usage_statistics_service,
)
from src.db.session import get_db
from src.schemas.administration.client_usage_statistics import (
    ClientUsageStatisticsCreate,
    ClientUsageStatisticsResponse,
    ClientUsageStatisticsUpdate,
)
from src.services.administration.client_usage_statistics import (
    ClientUsageStatisticsService,
)

router = APIRouter(
    prefix="/client-usage-statistics",
    tags=["Client Usage Statistics"],
)


@router.post(
    "",
    response_model=ClientUsageStatisticsResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_client_usage_statistics(
    statistics_data: ClientUsageStatisticsCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientUsageStatisticsService,
        Depends(get_client_usage_statistics_service),
    ],
) -> ClientUsageStatisticsResponse:
    """Create client usage statistics."""

    return service.create_client_usage_statistics(
        db=db,
        statistics_data=statistics_data,
    )


@router.get(
    "",
    response_model=list[ClientUsageStatisticsResponse],
)
def get_all_client_usage_statistics(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientUsageStatisticsService,
        Depends(get_client_usage_statistics_service),
    ],
) -> list[ClientUsageStatisticsResponse]:
    """Return all client usage statistics."""

    return service.get_all_client_usage_statistics(db)


@router.get(
    "/{statistics_id}",
    response_model=ClientUsageStatisticsResponse,
)
def get_client_usage_statistics(
    statistics_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientUsageStatisticsService,
        Depends(get_client_usage_statistics_service),
    ],
) -> ClientUsageStatisticsResponse:
    """Return client usage statistics by ID."""

    return service.get_client_usage_statistics(
        db=db,
        statistics_id=statistics_id,
    )


@router.get(
    "/client/{client_id}",
    response_model=list[ClientUsageStatisticsResponse],
)
def get_client_usage_statistics_by_client(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientUsageStatisticsService,
        Depends(get_client_usage_statistics_service),
    ],
) -> list[ClientUsageStatisticsResponse]:
    """Return usage statistics for a client."""

    return service.get_client_usage_statistics_by_client(
        db=db,
        client_id=client_id,
    )


@router.put(
    "/{statistics_id}",
    response_model=ClientUsageStatisticsResponse,
)
def update_client_usage_statistics(
    statistics_id: int,
    statistics_data: ClientUsageStatisticsUpdate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientUsageStatisticsService,
        Depends(get_client_usage_statistics_service),
    ],
) -> ClientUsageStatisticsResponse:
    """Update client usage statistics."""

    return service.update_client_usage_statistics(
        db=db,
        statistics_id=statistics_id,
        statistics_data=statistics_data,
    )