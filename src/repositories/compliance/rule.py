from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.rule import Rule
from src.repositories.base_repository import BaseRepository


class RuleRepository(BaseRepository[Rule]):
    """Repository for Rule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(Rule)

    def get_by_rule_code(
        self,
        db: Session,
        rule_code: str,
    ) -> Rule | None:
        return db.scalar(
            select(Rule).where(
                Rule.rule_code == rule_code
            )
        )