from src.exceptions.base import AppException


class TravelAuthorizationRuleAlreadyExistsError(
    AppException,
):
    """Raised when a travel authorization rule already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Travel Authorization Rule with {field} "
            f"'{value}' already exists."
        )


class TravelAuthorizationRuleNotFoundError(
    AppException,
):
    """Raised when a travel authorization rule cannot be found."""

    def __init__(
        self,
        travel_authorization_rule_id: int,
    ) -> None:
        self.travel_authorization_rule_id = (
            travel_authorization_rule_id
        )

        super().__init__(
            "Travel Authorization Rule with id "
            f"{travel_authorization_rule_id} "
            "was not found."
        )