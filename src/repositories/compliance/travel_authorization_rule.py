from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.travel_authorization_rule import (
    TravelAuthorizationRule,
)
from src.repositories.base_repository import BaseRepository


class TravelAuthorizationRuleRepository(
    BaseRepository[TravelAuthorizationRule],
):
    """Repository for TravelAuthorizationRule-specific database operations."""

    def __init__(self) -> None:
        super().__init__(TravelAuthorizationRule)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> TravelAuthorizationRule | None:
        return db.scalar(
            select(TravelAuthorizationRule).where(
                TravelAuthorizationRule.rule_id == rule_id
            )
        )