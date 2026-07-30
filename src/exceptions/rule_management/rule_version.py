from src.exceptions.base import AppException


class RuleVersionAlreadyExistsError(AppException):
    """Raised when a rule version already exists."""

    def __init__(
        self,
        rule_id: int,
        version_number: str,
    ):
        self.rule_id = rule_id
        self.version_number = version_number

        super().__init__(
            f"Rule version '{version_number}' already exists for rule {rule_id}."
        )


class RuleVersionNotFoundError(AppException):
    """Raised when a rule version cannot be found."""

    def __init__(
        self,
        rule_version_id: int,
    ):
        self.rule_version_id = rule_version_id

        super().__init__(
            f"Rule version with id {rule_version_id} was not found."
        )