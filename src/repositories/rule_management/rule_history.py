from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rule_management.rule_history import RuleHistory
from src.repositories.base_repository import BaseRepository


class RuleHistoryRepository(BaseRepository[RuleHistory]):
    """Repository for Rule History."""

    def __init__(self) -> None:
        super().__init__(RuleHistory)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleHistory]:
        """Return all history entries for a rule."""

        return list(
            db.scalars(
                select(RuleHistory)
                .where(
                    RuleHistory.rule_id == rule_id
                )
                .order_by(
                    RuleHistory.created_at.desc()
                )
            )
        )