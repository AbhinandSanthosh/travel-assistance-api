from src.exceptions.base import AppException


class HealthRuleAlreadyExistsError(
    AppException,
):
    """Raised when a health rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Health Rule with {field} "
            f"'{value}' already exists."
        )


class HealthRuleNotFoundError(
    AppException,
):
    """Raised when a health rule cannot be found."""

    def __init__(
        self,
        health_rule_id: int,
    ) -> None:
        self.health_rule_id = health_rule_id

        super().__init__(
            "Health Rule with id "
            f"{health_rule_id} "
            "was not found."
        )