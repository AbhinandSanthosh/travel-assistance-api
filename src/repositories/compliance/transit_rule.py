from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.transit_rule import TransitRule
from src.repositories.base_repository import BaseRepository


class TransitRuleRepository(
    BaseRepository[TransitRule],
):
    """Repository for TransitRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(TransitRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> TransitRule | None:
        return db.scalar(
            select(TransitRule).where(
                TransitRule.rule_id == rule_id
            )
        )