from src.exceptions.base import AppException


class RuleStatusAlreadyExistsError(AppException):
    """Raised when a rule status already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(
            f"Rule Status with {field} '{value}' already exists."
        )


class RuleStatusNotFoundError(AppException):
    """Raised when a rule status cannot be found."""

    def __init__(self, rule_status_id: int):
        self.rule_status_id = rule_status_id
        super().__init__(
            f"Rule Status with id {rule_status_id} was not found."
        )