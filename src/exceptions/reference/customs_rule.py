from src.exceptions.base import AppException


class CustomsRuleAlreadyExistsError(
    AppException,
):
    """Raised when a customs rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Customs Rule with {field} "
            f"'{value}' already exists."
        )


class CustomsRuleNotFoundError(
    AppException,
):
    """Raised when a customs rule cannot be found."""

    def __init__(
        self,
        customs_rule_id: int,
    ) -> None:
        self.customs_rule_id = customs_rule_id

        super().__init__(
            "Customs Rule with id "
            f"{customs_rule_id} "
            "was not found."
        )