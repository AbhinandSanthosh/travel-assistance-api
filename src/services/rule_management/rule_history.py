from sqlalchemy.orm import Session

from src.exceptions.rule_management.rule_history import (
    RuleHistoryNotFoundError,
)
from src.models.rule_management.rule_history import RuleHistory
from src.repositories.rule_management.rule_history import (
    RuleHistoryRepository,
)
from src.services.base_crud_service import BaseCrudService


class RuleHistoryService:
    """Service layer for Rule History."""

    def __init__(
        self,
        rule_history_repository: RuleHistoryRepository,
    ) -> None:
        self.rule_history_repository = rule_history_repository
        self.base_crud = BaseCrudService(rule_history_repository)

    def get_rule_history(
        self,
        db: Session,
        history_id: int,
    ) -> RuleHistory:
        """Retrieve a rule history record by ID."""

        history = self.base_crud.get_by_id(
            db=db,
            obj_id=history_id,
        )

        if history is None:
            raise RuleHistoryNotFoundError(history_id)

        return history

    def get_all_rule_history(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RuleHistory]:
        """Retrieve all rule history records."""


        return self.base_crud.get_all(db, skip, limit)

    def get_rule_history_by_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> list[RuleHistory]:
        """Retrieve history for a specific rule."""

        return self.rule_history_repository.get_by_rule_id(
            db=db,
            rule_id=rule_id,
        )