from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.passport_rule import PassportRule
from src.repositories.base_repository import BaseRepository


class PassportRuleRepository(
    BaseRepository[PassportRule],
):
    """Repository for PassportRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(PassportRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> PassportRule | None:
        return db.scalar(
            select(PassportRule).where(
                PassportRule.rule_id == rule_id
            )
        )