from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rule_management.rule_status import RuleStatus
from src.repositories.base_repository import BaseRepository


class RuleStatusRepository(BaseRepository[RuleStatus]):
    """Repository for RuleStatus-specific database operations."""

    def __init__(self) -> None:
        super().__init__(RuleStatus)

    def get_by_status_code(
        self,
        db: Session,
        status_code: str,
    ) -> RuleStatus | None:
        return db.scalar(
            select(RuleStatus).where(
                RuleStatus.status_code == status_code
            )
        )