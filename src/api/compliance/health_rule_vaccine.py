from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_health_rule_vaccine_service,
)
from src.db.session import get_db
from src.schemas.compliance.health_rule_vaccine import (
    HealthRuleVaccineCreate,
    HealthRuleVaccineResponse,
    HealthRuleVaccineUpdate,
)
from src.services.compliance.health_rule_vaccine import (
    HealthRuleVaccineService,
)

router = APIRouter(
    prefix="/health-rule-vaccines",
    tags=["Health Rule Vaccines"],
)


@router.post(
    "",
    response_model=HealthRuleVaccineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_health_rule_vaccine(
    health_rule_vaccine_data: HealthRuleVaccineCreate,
    db: Session = Depends(get_db),
    service: HealthRuleVaccineService = Depends(
        get_health_rule_vaccine_service,
    ),
) -> HealthRuleVaccineResponse:
    """Create a new health rule vaccine."""
    return service.create_health_rule_vaccine(
        db,
        health_rule_vaccine_data,
    )


@router.get(
    "",
    response_model=list[HealthRuleVaccineResponse],
)
def get_all_health_rule_vaccines(
    db: Session = Depends(get_db),
    service: HealthRuleVaccineService = Depends(
        get_health_rule_vaccine_service,
    ),
) -> list[HealthRuleVaccineResponse]:
    """Retrieve all health rule vaccines."""
    return service.get_all_health_rule_vaccines(
        db,
    )


@router.get(
    "/{health_rule_vaccine_id}",
    response_model=HealthRuleVaccineResponse,
)
def get_health_rule_vaccine(
    health_rule_vaccine_id: int,
    db: Session = Depends(get_db),
    service: HealthRuleVaccineService = Depends(
        get_health_rule_vaccine_service,
    ),
) -> HealthRuleVaccineResponse:
    """Retrieve a health rule vaccine by ID."""
    return service.get_health_rule_vaccine(
        db,
        health_rule_vaccine_id,
    )


@router.put(
    "/{health_rule_vaccine_id}",
    response_model=HealthRuleVaccineResponse,
)
def update_health_rule_vaccine(
    health_rule_vaccine_id: int,
    health_rule_vaccine_data: HealthRuleVaccineUpdate,
    db: Session = Depends(get_db),
    service: HealthRuleVaccineService = Depends(
        get_health_rule_vaccine_service,
    ),
) -> HealthRuleVaccineResponse:
    """Update an existing health rule vaccine."""
    return service.update_health_rule_vaccine(
        db=db,
        health_rule_vaccine_id=health_rule_vaccine_id,
        health_rule_vaccine_data=health_rule_vaccine_data,
    )


@router.delete(
    "/{health_rule_vaccine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_health_rule_vaccine(
    health_rule_vaccine_id: int,
    db: Session = Depends(get_db),
    service: HealthRuleVaccineService = Depends(
        get_health_rule_vaccine_service,
    ),
) -> Response:
    """Delete a health rule vaccine."""
    service.delete_health_rule_vaccine(
        db,
        health_rule_vaccine_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )