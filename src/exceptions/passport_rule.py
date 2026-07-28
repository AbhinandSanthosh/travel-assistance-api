from src.exceptions.base import AppException


class PassportRuleAlreadyExistsError(
    AppException,
):
    """Raised when a passport rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Passport Rule with {field} "
            f"'{value}' already exists."
        )


class PassportRuleNotFoundError(
    AppException,
):
    """Raised when a passport rule cannot be found."""

    def __init__(
        self,
        passport_rule_id: int,
    ) -> None:
        self.passport_rule_id = passport_rule_id

        super().__init__(
            "Passport Rule with id "
            f"{passport_rule_id} "
            "was not found."
        )