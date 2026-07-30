from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_audit_log_service,
)
from src.db.session import get_db
from src.schemas.administration.audit_log import (
    AuditLogCreate,
    AuditLogResponse,
)
from src.services.administration.audit_log import (
    AuditLogService,
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.post(
    "",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_audit_log(
    audit_log_data: AuditLogCreate,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
) -> AuditLogResponse:
    """Create an audit log."""

    return service.create_audit_log(
        db=db,
        audit_log_data=audit_log_data,
    )


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def get_all_audit_logs(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
) -> list[AuditLogResponse]:
    """Return all audit logs."""

    return service.get_all_audit_logs(db)


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(
    audit_log_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
) -> AuditLogResponse:
    """Return an audit log by ID."""

    return service.get_audit_log(
        db=db,
        audit_log_id=audit_log_id,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[AuditLogResponse],
)
def get_audit_logs_by_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[
        AuditLogService,
        Depends(get_audit_log_service),
    ],
) -> list[AuditLogResponse]:
    """Return audit logs for a user."""

    return service.get_audit_logs_by_user(
        db=db,
        user_id=user_id,
    )