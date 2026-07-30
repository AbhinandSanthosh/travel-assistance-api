from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_api_client_service,
)
from src.db.session import get_db  # ⚠️ Use your project's actual get_db import
from src.schemas.administration.api_client import (
    APIClientCreate,
    APIClientResponse,
    APIClientUpdate,
)
from src.services.administration.api_client import (
    APIClientService,
)

router = APIRouter(
    prefix="/api-clients",
    tags=["API Clients"],
)


@router.post(
    "",
    response_model=APIClientResponse,
)
def create_api_client(
    client: APIClientCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIClientService,
        Depends(get_api_client_service),
    ],
):
    """Create an API client."""

    return service.create_api_client(
        db=db,
        client_data=client,
    )


@router.get(
    "",
    response_model=list[APIClientResponse],
)
def get_all_api_clients(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIClientService,
        Depends(get_api_client_service),
    ],
):
    """Return all API clients."""

    return service.get_all_api_clients(db=db)


@router.get(
    "/{client_id}",
    response_model=APIClientResponse,
)
def get_api_client(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIClientService,
        Depends(get_api_client_service),
    ],
):
    """Return an API client by ID."""

    return service.get_api_client(
        db=db,
        client_id=client_id,
    )


@router.put(
    "/{client_id}",
    response_model=APIClientResponse,
)
def update_api_client(
    client_id: int,
    client: APIClientUpdate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIClientService,
        Depends(get_api_client_service),
    ],
):
    """Update an API client."""

    return service.update_api_client(
        db=db,
        client_id=client_id,
        client_data=client,
    )


@router.delete(
    "/{client_id}",
)
def delete_api_client(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        APIClientService,
        Depends(get_api_client_service),
    ],
):
    """Delete an API client."""

    service.delete_api_client(
        db=db,
        client_id=client_id,
    )

    return {
        "message": "API client deleted successfully."
    }