from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.audit_log import AuditLog
from src.repositories.base_repository import BaseRepository


class AuditLogRepository(
    BaseRepository[AuditLog]
):
    """Repository for Audit Log."""

    def __init__(self) -> None:
        super().__init__(AuditLog)

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[AuditLog]:
        """Return audit logs for a user."""

        return list(
            db.scalars(
                select(AuditLog).where(
                    AuditLog.user_id == user_id,
                )
            ).all()
        )