from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import get_autocheck_service
from src.db.session import get_db
from src.schemas.compliance.autocheck import (
    AutoCheckRequest,
    AutoCheckResponse,
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
    db: Session = Depends(get_db),
    service: AutoCheckService = Depends(get_autocheck_service),
) -> AutoCheckResponse:
   

    return service.run(db, payload, _client_ip(request))