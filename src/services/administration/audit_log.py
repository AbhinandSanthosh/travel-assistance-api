from sqlalchemy.orm import Session

from src.exceptions.administration.audit_log import (
    AuditLogNotFoundError,
)
from src.models.administration.audit_log import AuditLog
from src.repositories.administration.audit_log import (
    AuditLogRepository,
)
from src.schemas.administration.audit_log import (
    AuditLogCreate,
)
from src.services.base_crud_service import BaseCrudService


class AuditLogService:
    """Service for Audit Logs."""

    def __init__(
        self,
        repository: AuditLogRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(repository)

    def create_audit_log(
        self,
        db: Session,
        audit_log_data: AuditLogCreate,
    ) -> AuditLog:
        """Create an audit log."""

        return self.base_crud.create(
            db=db,
            obj_in=audit_log_data,
        )

    def get_audit_log(
        self,
        db: Session,
        audit_log_id: int,
    ) -> AuditLog:
        """Return an audit log by ID."""

        audit_log = self.base_crud.get_by_id(
            db=db,
            obj_id=audit_log_id,
        )

        if audit_log is None:
            raise AuditLogNotFoundError(
                audit_log_id,
            )

        return audit_log

    def get_all_audit_logs(
        self,
        db: Session,
    ) -> list[AuditLog]:
        """Return all audit logs."""

        return self.base_crud.get_all(db=db)

    def get_audit_logs_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:
        """Return all audit logs for a user."""

        return self.repository.get_by_user_id(
            db=db,
            user_id=user_id,
        )