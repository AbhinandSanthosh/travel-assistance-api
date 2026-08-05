from sqlalchemy.orm import Session

from src.exceptions.compliance.rule_execution_log import (
    RuleExecutionLogNotFoundError,
)
from src.models.compliance.rule_execution_log import (
    RuleExecutionLog,
)
from src.repositories.compliance.rule_execution_log import (
    RuleExecutionLogRepository,
)
from src.schemas.compliance.rule_execution_log import (
    RuleExecutionLogCreate,
    RuleExecutionLogUpdate,
)
from src.services.base_crud_service import (
    BaseCrudService,
)


class RuleExecutionLogService:
    """Service layer for RuleExecutionLog."""

    def __init__(
        self,
        repository: RuleExecutionLogRepository,
    ) -> None:
        self.repository = repository
        self.crud = BaseCrudService(
            repository,
        )

    def create_rule_execution_log(
        self,
        db: Session,
        rule_execution_log_data: RuleExecutionLogCreate,
    ) -> RuleExecutionLog:
        """Create a rule execution log."""

        return self.crud.create(
            db=db,
            model=RuleExecutionLog,
            data=rule_execution_log_data,
        )

    def get_rule_execution_log(
        self,
        db: Session,
        rule_execution_log_id: int,
    ) -> RuleExecutionLog:
        """Get a rule execution log by ID."""

        rule_execution_log = self.crud.get_by_id(
            db=db,
            obj_id=rule_execution_log_id,
        )

        if rule_execution_log is None:
            raise RuleExecutionLogNotFoundError()

        return rule_execution_log

    def get_rule_execution_logs(
        self,
        db: Session,
    ) -> list[RuleExecutionLog]:
        """Get all rule execution logs."""

        return self.crud.get_all(db)

    def update_rule_execution_log(
        self,
        db: Session,
        rule_execution_log_id: int,
        rule_execution_log_data: RuleExecutionLogUpdate,
    ) -> RuleExecutionLog:
        """Update a rule execution log."""

        rule_execution_log = self.get_rule_execution_log(
            db=db,
            rule_execution_log_id=rule_execution_log_id,
        )

        return self.crud.update(
            db=db,
            obj=rule_execution_log,
            data=rule_execution_log_data,
        )

    def delete_rule_execution_log(
        self,
        db: Session,
        rule_execution_log_id: int,
    ) -> None:
        """Delete a rule execution log."""

        rule_execution_log = self.get_rule_execution_log(
            db=db,
            rule_execution_log_id=rule_execution_log_id,
        )

        self.crud.delete(
            db=db,
            obj=rule_execution_log,
        )