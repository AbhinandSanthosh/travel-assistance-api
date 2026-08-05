from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_compliance_check_service,
)
from src.db.session import get_db
from src.schemas.compliance.compliance_check import (
    ComplianceCheckCreate,
    ComplianceCheckResponse,
    ComplianceCheckUpdate,
)
from src.services.compliance.compliance_check import (
    ComplianceCheckService,
)

router = APIRouter(
    prefix="/compliance-checks",
    tags=["Compliance Checks"],
)


@router.post(
    "",
    response_model=ComplianceCheckResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_compliance_check(
    data: ComplianceCheckCreate,
    db: Session = Depends(get_db),
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
):
    return service.create_compliance_check(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[ComplianceCheckResponse],
)
def get_compliance_checks(
    db: Session = Depends(get_db),
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
):
    return service.get_compliance_checks(db)


@router.get(
    "/{compliance_check_id}",
    response_model=ComplianceCheckResponse,
)
def get_compliance_check(
    compliance_check_id: int,
    db: Session = Depends(get_db),
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
):
    return service.get_compliance_check(
        db,
        compliance_check_id,
    )


@router.put(
    "/{compliance_check_id}",
    response_model=ComplianceCheckResponse,
)
def update_compliance_check(
    compliance_check_id: int,
    data: ComplianceCheckUpdate,
    db: Session = Depends(get_db),
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
):
    return service.update_compliance_check(
        db,
        compliance_check_id,
        data,
    )


@router.delete(
    "/{compliance_check_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_compliance_check(
    compliance_check_id: int,
    db: Session = Depends(get_db),
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
):
    service.delete_compliance_check(
        db,
        compliance_check_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )