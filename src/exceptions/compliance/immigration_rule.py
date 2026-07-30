from src.exceptions.base import AppException


class ImmigrationRuleAlreadyExistsError(
    AppException,
):
    """Raised when an immigration rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Immigration Rule with {field} "
            f"'{value}' already exists."
        )


class ImmigrationRuleNotFoundError(
    AppException,
):
    """Raised when an immigration rule cannot be found."""

    def __init__(
        self,
        immigration_rule_id: int,
    ) -> None:
        self.immigration_rule_id = immigration_rule_id

        super().__init__(
            "Immigration Rule with id "
            f"{immigration_rule_id} "
            "was not found."
        )