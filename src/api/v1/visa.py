from fastapi import (
    APIRouter,
    Depends,
    Header,
    Request,
    status,
)
from sqlalchemy.orm import Session

from src.core.client_ip import get_client_ip
from src.db.session import get_db
from src.schemas.v1.travel_requirements import (
    TravelRequirementsCheckRequest,
    TravelRequirementsCheckResponse,
)
from src.services.v1.travel_requirements_service import (
    TravelRequirementsService,
)
from src.api.dependencies.v1 import (
    get_travel_requirements_service,
)


router = APIRouter(
    prefix="/api/v1/visa",
    tags=["Visa (v1)"],
)


@router.post(
    "/check",
    response_model=TravelRequirementsCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate visa requirements for a passenger journey",
)
def check_visa(
    payload: TravelRequirementsCheckRequest,
    request: Request,
    x_api_key: str = Header(
        ...,
        alias="X-API-Key",
    ),
    db: Session = Depends(get_db),
    service: TravelRequirementsService = Depends(
        get_travel_requirements_service,
    ),
) -> TravelRequirementsCheckResponse:

    return service.check(
        db=db,
        payload=payload,
        client_ip=get_client_ip(request),
        api_key=x_api_key,
        domains=["VISA"],
    )
