from src.exceptions.base import AppException


class RuleExecutionLogNotFoundError(
    AppException,
):
    """Raised when a rule execution log is not found."""

    def __init__(self) -> None:
        super().__init__(
            message="Rule Execution Log not found.",
            code="RULE_EXECUTION_LOG_NOT_FOUND",
            status_code=404,
        )