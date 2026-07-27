from src.exceptions.base import AppException


class VisaRuleAlreadyExistsError(AppException):
    """Raised when a visa rule already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Visa Rule with {field} '{value}' already exists.")


class VisaRuleNotFoundError(AppException):
    """Raised when a visa rule cannot be found."""

    def __init__(self, visa_rule_id: int):
        self.visa_rule_id = visa_rule_id
        super().__init__(f"Visa Rule with id {visa_rule_id} was not found.")