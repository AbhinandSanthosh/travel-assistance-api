from src.exceptions.base import AppException


class TransitRuleAlreadyExistsError(
    AppException,
):
    """Raised when a transit rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Transit Rule with {field} "
            f"'{value}' already exists."
        )


class TransitRuleNotFoundError(
    AppException,
):
    """Raised when a transit rule cannot be found."""

    def __init__(
        self,
        transit_rule_id: int,
    ) -> None:
        self.transit_rule_id = transit_rule_id

        super().__init__(
            "Transit Rule with id "
            f"{transit_rule_id} "
            "was not found."
        )