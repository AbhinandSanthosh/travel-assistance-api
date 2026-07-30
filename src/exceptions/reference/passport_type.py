from src.exceptions.base import AppException


class PassportTypeAlreadyExistsError(AppException):
    """Raised when a passport type already exists."""

    def __init__(self, field: str, value: str):
        super().__init__(
            f"Passport type with {field} '{value}' already exists."
        )


class PassportTypeNotFoundError(AppException):
    """Raised when a passport type is not found."""

    def __init__(self, passport_type_id: int):
        super().__init__(
            f"Passport type with ID {passport_type_id} not found."
        )