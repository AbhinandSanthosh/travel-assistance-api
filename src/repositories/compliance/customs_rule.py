from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.customs_rule import (
    CustomsRule,
)
from src.repositories.base_repository import (
    BaseRepository,
)


class CustomsRuleRepository(
    BaseRepository[CustomsRule],
):
    """Repository for CustomsRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(CustomsRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> CustomsRule | None:
        return db.scalar(
            select(CustomsRule).where(
                CustomsRule.rule_id == rule_id
            )
        )