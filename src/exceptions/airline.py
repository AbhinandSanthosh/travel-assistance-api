from src.exceptions.base import AppException


class AirlineAlreadyExistsError(AppException):
    """Raised when an airline already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"Airline with {field} '{value}' already exists."
        )


class AirlineNotFoundError(AppException):
    """Raised when an airline cannot be found."""

    def __init__(
        self,
        airline_id: int,
    ):
        self.airline_id = airline_id
        super().__init__(
            f"Airline with id {airline_id} was not found."
        )