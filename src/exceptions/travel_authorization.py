from src.exceptions.base import AppException


class TravelAuthorizationAlreadyExistsError(AppException):
    """Raised when a travel authorization already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"TravelAuthorization with {field} '{value}' already exists."
        )


class TravelAuthorizationNotFoundError(AppException):
    """Raised when a travel authorization cannot be found."""

    def __init__(
        self,
        travel_authorization_id: int,
    ):
        self.travel_authorization_id = travel_authorization_id
        super().__init__(
            "TravelAuthorization with id "
            f"{travel_authorization_id} was not found."
        )