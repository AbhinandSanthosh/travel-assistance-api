from src.exceptions.base import AppException


class RuleAlreadyExistsError(AppException):
    """Raised when a rule already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Rule with {field} '{value}' already exists.")


class RuleNotFoundError(AppException):
    """Raised when a rule cannot be found."""

    def __init__(self, rule_id: int):
        self.rule_id = rule_id
        super().__init__(f"Rule with id {rule_id} was not found.")