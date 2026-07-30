from src.exceptions.base import AppException


class AirportAlreadyExistsError(AppException):
    """Raised when an airport already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"Airport with {field} '{value}' already exists."
        )


class AirportNotFoundError(AppException):
    """Raised when an airport cannot be found."""

    def __init__(
        self,
        airport_id: int,
    ):
        self.airport_id = airport_id
        super().__init__(
            f"Airport with id {airport_id} was not found."
        )