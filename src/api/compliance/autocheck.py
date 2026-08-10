from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import get_autocheck_service
from src.db.session import get_db
from src.schemas.compliance.autocheck import (
    AutoCheckRequest,
    AutoCheckResponse,
    ValidateKeyResponse,
)
from src.services.compliance.autocheck_service import AutoCheckService

router = APIRouter(
    prefix="/autocheck",
    tags=["Auto Check"],
)


def _client_ip(request: Request) -> str:
    """Prefer X-Forwarded-For (behind a proxy/load balancer), fall back
    to the direct connecting socket address."""

    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.client.host if request.client else "unknown"


@router.post(
    "",
    response_model=AutoCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Run an automated compliance check for a traveller",
)
def run_autocheck(
    payload: AutoCheckRequest,
    request: Request,
    x_api_key: str = Header(
        ...,
        alias="X-API-Key",
        description="API key identifying the calling client.",
    ),
    db: Session = Depends(get_db),
    service: AutoCheckService = Depends(get_autocheck_service),
) -> AutoCheckResponse:

    return service.run(db, payload, _client_ip(request), x_api_key)


@router.post(
    "/validate-key",
    response_model=ValidateKeyResponse,
    status_code=status.HTTP_200_OK,
    summary="Check whether an API key is valid, active, and whitelisted",
)
def validate_key(
    request: Request,
    x_api_key: str = Header(
        ...,
        alias="X-API-Key",
        description="API key to validate.",
    ),
    db: Session = Depends(get_db),
    service: AutoCheckService = Depends(get_autocheck_service),
) -> ValidateKeyResponse:
    """Runs the same key/status/IP-whitelist checks /autocheck itself
    does (minus rate limiting, so this never eats into the client's
    actual quota) without running the rule engine. Lets the frontend
    confirm a key works right when it's entered, instead of only
    finding out on the first real submission."""

    client = service.validate_key(db, x_api_key, _client_ip(request))
    return ValidateKeyResponse(
        client_name=client.client_name,
        company_name=client.company_name,
    )