from fastapi import APIRouter, Depends, status

from src.api.dependencies.compliance import (
    get_compliance_check_service,
)
from src.models.compliance.compliance_check import (
    ComplianceCheck,
)
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
    "/",
    response_model=ComplianceCheckResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_compliance_check(
    data: ComplianceCheckCreate,
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
) -> ComplianceCheck:
    return await service.create_compliance_check(data)


@router.get(
    "/",
    response_model=list[ComplianceCheckResponse],
)
async def get_compliance_checks(
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
) -> list[ComplianceCheck]:
    return await service.get_compliance_checks()


@router.get(
    "/{compliance_check_id}",
    response_model=ComplianceCheckResponse,
)
async def get_compliance_check(
    compliance_check_id: int,
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
) -> ComplianceCheck:
    return await service.get_compliance_check(
        compliance_check_id,
    )


@router.put(
    "/{compliance_check_id}",
    response_model=ComplianceCheckResponse,
)
async def update_compliance_check(
    compliance_check_id: int,
    data: ComplianceCheckUpdate,
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
) -> ComplianceCheck:
    return await service.update_compliance_check(
        compliance_check_id,
        data,
    )


@router.delete(
    "/{compliance_check_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_compliance_check(
    compliance_check_id: int,
    service: ComplianceCheckService = Depends(
        get_compliance_check_service,
    ),
) -> None:
    await service.delete_compliance_check(
        compliance_check_id,
    )