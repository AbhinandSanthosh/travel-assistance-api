from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.health_rule import HealthRule
from src.repositories.base_repository import BaseRepository


class HealthRuleRepository(
    BaseRepository[HealthRule],
):
    """Repository for HealthRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(HealthRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> HealthRule | None:
        return db.scalar(
            select(HealthRule).where(
                HealthRule.rule_id == rule_id
            )
        )