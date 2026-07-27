from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.visa_rule import VisaRule
from src.repositories.base_repository import BaseRepository


class VisaRuleRepository(BaseRepository[VisaRule]):
    """Repository for VisaRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(VisaRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> VisaRule | None:
        return db.scalar(
            select(VisaRule).where(
                VisaRule.rule_id == rule_id
            )
        )