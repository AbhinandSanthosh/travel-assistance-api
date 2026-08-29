from sqlalchemy.orm import Session

from src.exceptions.rule_management.rule_approval import (
    RuleApprovalAlreadyExistsError,
    RuleApprovalNotFoundError,
)
from src.models.rule_management.rule_approval import RuleApproval
from src.repositories.rule_management.rule_approval import (
    RuleApprovalRepository,
)
from src.schemas.rule_management.rule_approval import (
    RuleApprovalCreate,
)
from src.services.base_crud_service import BaseCrudService


class RuleApprovalService:
    """Service for Rule Approval."""

    def __init__(self) -> None:
        self.repository = RuleApprovalRepository()
        self.base_crud = BaseCrudService(self.repository)

    def create_rule_approval(
        self,
        db: Session,
        approval_data: RuleApprovalCreate,
    ) -> RuleApproval:
        """Create a new rule approval."""

        existing_approval = self.repository.get_by_rule_and_reviewer(
            db=db,
            rule_id=approval_data.rule_id,
            reviewer_id=approval_data.reviewer_id,
        )

        if existing_approval:
            raise RuleApprovalAlreadyExistsError(
                rule_id=approval_data.rule_id,
                reviewer_id=approval_data.reviewer_id,
            )

        return self.base_crud.create(
            db=db,
            obj_in=approval_data,
        )

    def get_rule_approval(
        self,
        db: Session,
        approval_id: int,
    ) -> RuleApproval:
        """Return a rule approval by ID."""

        approval = self.base_crud.get_by_id(
            db=db,
            obj_id=approval_id,
        )

        if approval is None:
            raise RuleApprovalNotFoundError(approval_id)

        return approval

    def get_all_rule_approvals(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RuleApproval]:
        """Return all rule approvals."""

        return self.base_crud.get_all(db=db, skip=skip, limit=limit)

    def get_rule_approvals_by_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleApproval]:
        """Return all approvals for a rule."""

        return self.repository.get_by_rule_id(
            db=db,
            rule_id=rule_id,
        )