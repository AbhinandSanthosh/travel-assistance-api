from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.immigration_rule import (
    ImmigrationRule,
)
from src.repositories.base_repository import (
    BaseRepository,
)


class ImmigrationRuleRepository(
    BaseRepository[ImmigrationRule],
):
    """Repository for ImmigrationRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(ImmigrationRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> ImmigrationRule | None:
        return db.scalar(
            select(ImmigrationRule).where(
                ImmigrationRule.rule_id == rule_id
            )
        )