from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.rule_management.rule_approval import RuleApproval
from src.repositories.base_repository import BaseRepository


class RuleApprovalRepository(BaseRepository[RuleApproval]):
    """Repository for Rule Approval."""

    def __init__(self) -> None:
        super().__init__(RuleApproval)

    def get_by_rule_and_reviewer(
        self,
        db: Session,
        rule_id: int,
        reviewer_id: int,
    ) -> RuleApproval | None:
        """Return an approval by rule and reviewer."""

        return db.scalar(
            select(RuleApproval).where(
                RuleApproval.rule_id == rule_id,
                RuleApproval.reviewer_id == reviewer_id,
            )
        )

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleApproval]:
        """Return all approvals for a rule."""

        return list(
            db.scalars(
                select(RuleApproval).where(
                    RuleApproval.rule_id == rule_id
                )
            )
        )