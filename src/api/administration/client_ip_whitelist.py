from typing import Annotated
from src.api.dependencies.auth import require_permission

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_client_ip_whitelist_service,
)
from src.db.session import get_db  # Use the same import used by your existing routers
from src.schemas.administration.client_ip_whitelist import (
    ClientIPWhitelistCreate,
    ClientIPWhitelistResponse,
    ClientIPWhitelistUpdate,
)
from src.services.administration.client_ip_whitelist import (
    ClientIPWhitelistService,
)

router = APIRouter(
    prefix="/client-ip-whitelists",
    tags=["Client IP Whitelists"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=ClientIPWhitelistResponse,
)
def create_client_ip_whitelist(
    whitelist: ClientIPWhitelistCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Create a client IP whitelist entry."""

    return service.create_client_ip_whitelist(
        db=db,
        whitelist_data=whitelist,
    )


@router.get(
    "",
    response_model=list[ClientIPWhitelistResponse],
)
def get_all_client_ip_whitelists(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Return all client IP whitelist entries."""

    return service.get_all_client_ip_whitelists(db=db)


@router.get(
    "/{whitelist_id}",
    response_model=ClientIPWhitelistResponse,
)
def get_client_ip_whitelist(
    whitelist_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Return a client IP whitelist entry by ID."""

    return service.get_client_ip_whitelist(
        db=db,
        whitelist_id=whitelist_id,
    )


@router.get(
    "/client/{client_id}",
    response_model=list[ClientIPWhitelistResponse],
)
def get_client_whitelist_entries(
    client_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Return whitelist entries for an API client."""

    return service.get_client_whitelist_entries(
        db=db,
        client_id=client_id,
    )


@router.put(
    "/{whitelist_id}",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=ClientIPWhitelistResponse,
)
def update_client_ip_whitelist(
    whitelist_id: int,
    whitelist: ClientIPWhitelistUpdate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Update a client IP whitelist entry."""

    return service.update_client_ip_whitelist(
        db=db,
        whitelist_id=whitelist_id,
        whitelist_data=whitelist,
    )


@router.delete(
    "/{whitelist_id}",
    dependencies=[Depends(require_permission("administration.write"))],
)
def delete_client_ip_whitelist(
    whitelist_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        ClientIPWhitelistService,
        Depends(get_client_ip_whitelist_service),
    ],
):
    """Delete a client IP whitelist entry."""

    service.delete_client_ip_whitelist(
        db=db,
        whitelist_id=whitelist_id,
    )

    return {
        "message": "Client IP whitelist entry deleted successfully."
    }