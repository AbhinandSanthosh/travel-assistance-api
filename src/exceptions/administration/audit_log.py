from src.exceptions.base import AppException


class AuditLogNotFoundError(AppException):
    """Raised when an audit log cannot be found."""

    def __init__(
        self,
        audit_log_id: int,
    ):
        self.audit_log_id = audit_log_id

        super().__init__(
            f"Audit log with id {audit_log_id} was not found."
        )