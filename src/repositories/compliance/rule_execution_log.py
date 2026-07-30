from src.models.compliance.rule_execution_log import (
    RuleExecutionLog,
)
from src.repositories.base_repository import BaseRepository


class RuleExecutionLogRepository(
    BaseRepository[RuleExecutionLog]
):
    """Repository for Rule Execution Log."""

    def __init__(self) -> None:
        super().__init__(RuleExecutionLog)