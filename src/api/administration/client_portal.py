from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import get_client_portal_service
from src.api.dependencies.client_portal import get_current_portal_client
from src.db.session import get_db
from src.models.administration.api_client import APIClient
from src.schemas.administration.client_portal import (
    APIKeyStatusResponse,
    ClientLoginRequest,
    ClientPortalMeResponse,
    ClientPortalTokenResponse,
    ClientSignupRequest,
    ClientSignupResponse,
    GeneratedAPIKeyResponse,
)
from src.services.administration.client_portal_service import (
    ClientPortalService,
)

router = APIRouter(
    prefix="/api/v1/client-portal",
    tags=["Client Portal"],
)

ServiceDep = Annotated[
    ClientPortalService,
    Depends(get_client_portal_service),
]

DbDep = Annotated[
    Session,
    Depends(get_db),
]

CurrentClientDep = Annotated[
    APIClient,
    Depends(get_current_portal_client),
]


@router.post(
    "/signup",
    response_model=ClientSignupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new client account (no API key yet)",
)
def signup(
    payload: ClientSignupRequest,
    db: DbDep,
    service: ServiceDep,
) -> ClientSignupResponse:
    """Create a client portal account.

    This only creates the account and issues login credentials.
    It deliberately does NOT hand back an API key.

    The client logs in afterwards and calls POST /api-key
    to generate one.
    """

    client = service.signup(db, payload)

    return ClientSignupResponse(
        client_code=client.client_code,
        company_name=client.company_name,
        contact_email=client.contact_email,
    )


@router.post(
    "/login",
    response_model=ClientPortalTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Client portal login (JWT)",
)
def login(
    payload: ClientLoginRequest,
    db: DbDep,
    service: ServiceDep,
) -> ClientPortalTokenResponse:
    """Authenticate a client contact and issue a portal session token.

    This token is only valid against /api/v1/client-portal/*
    endpoints. It is not an API key and cannot be used against
    /autocheck.
    """

    client = service.login(
        db,
        payload.contact_email,
        payload.password,
    )

    token, expires_in = service.issue_portal_token(client)

    return ClientPortalTokenResponse(
        access_token=token,
        expires_in=expires_in,
    )


@router.get(
    "/me",
    response_model=ClientPortalMeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated client account",
)
def read_current_client(
    client: CurrentClientDep,
) -> ClientPortalMeResponse:
    return ClientPortalMeResponse.model_validate(client)


@router.post(
    "/api-key",
    response_model=GeneratedAPIKeyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate (or rotate) this client's live API key",
)
def generate_api_key(
    request: Request,
    client: CurrentClientDep,
    db: DbDep,
    service: ServiceDep,
) -> GeneratedAPIKeyResponse:
    """Generate a new API key and automatically whitelist
    the IP address used to generate it.

    The full API key is returned exactly once.
    """

    forwarded = request.headers.get("x-forwarded-for")

    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else None

    return service.generate_api_key(
        db=db,
        client=client,
        client_ip=client_ip,
    )


@router.get(
    "/api-key",
    response_model=APIKeyStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get masked status of this client's current API key",
)
def get_api_key_status(
    client: CurrentClientDep,
    service: ServiceDep,
) -> APIKeyStatusResponse:
    return service.get_api_key_status(client)


@router.delete(
    "/api-key",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke this client's current API key",
)
def revoke_api_key(
    client: CurrentClientDep,
    db: DbDep,
    service: ServiceDep,
) -> None:
    """Revoke the current key immediately.

    Any application still using it will start getting 401s from
    /autocheck until a new key is generated.
    """

    service.revoke_api_key(db, client)