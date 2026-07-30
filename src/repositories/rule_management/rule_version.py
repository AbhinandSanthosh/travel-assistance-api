from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rule_management.rule_version import RuleVersion
from src.repositories.base_repository import BaseRepository


class RuleVersionRepository(BaseRepository[RuleVersion]):
    """Repository for Rule Version-specific database operations."""

    def __init__(self) -> None:
        super().__init__(RuleVersion)

    def get_by_rule_and_version(
        self,
        db: Session,
        rule_id: int,
        version_number: str,
    ) -> RuleVersion | None:
        return db.scalar(
            select(RuleVersion).where(
                RuleVersion.rule_id == rule_id,
                RuleVersion.version_number == version_number,
            )
        )