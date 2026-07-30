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
from src.services.base_crud_service import BaseCrudService


class RuleExecutionLogService:
    """Service for Rule Execution Log."""

    def __init__(
        self,
        repository: RuleExecutionLogRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(
            repository,
        )

    async def create_rule_execution_log(
        self,
        data: RuleExecutionLogCreate,
    ) -> RuleExecutionLog:
        return await self.base_crud.create(data)

    async def get_rule_execution_log(
        self,
        rule_execution_log_id: int,
    ) -> RuleExecutionLog:
        rule_execution_log = (
            await self.base_crud.get_by_id(
                rule_execution_log_id,
            )
        )

        if rule_execution_log is None:
            raise RuleExecutionLogNotFoundError()

        return rule_execution_log

    async def get_rule_execution_logs(
        self,
    ) -> list[RuleExecutionLog]:
        return await self.base_crud.get_all()

    async def update_rule_execution_log(
        self,
        rule_execution_log_id: int,
        data: RuleExecutionLogUpdate,
    ) -> RuleExecutionLog:
        rule_execution_log = (
            await self.base_crud.get_by_id(
                rule_execution_log_id,
            )
        )

        if rule_execution_log is None:
            raise RuleExecutionLogNotFoundError()

        return await self.base_crud.update(
            rule_execution_log,
            data,
        )

    async def delete_rule_execution_log(
        self,
        rule_execution_log_id: int,
    ) -> None:
        rule_execution_log = (
            await self.base_crud.get_by_id(
                rule_execution_log_id,
            )
        )

        if rule_execution_log is None:
            raise RuleExecutionLogNotFoundError()

        await self.base_crud.delete(
            rule_execution_log,
        )