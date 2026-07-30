from src.exceptions.base import AppException


class PassengerTypeAlreadyExistsError(AppException):
    """Raised when a passenger type already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"PassengerType with {field} '{value}' already exists."
        )


class PassengerTypeNotFoundError(AppException):
    """Raised when a passenger type cannot be found."""

    def __init__(
        self,
        passenger_type_id: int,
    ):
        self.passenger_type_id = passenger_type_id
        super().__init__(
            f"PassengerType with id {passenger_type_id} was not found."
        )