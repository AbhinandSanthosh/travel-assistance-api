from src.exceptions.base import AppException


class VisaTypeAlreadyExistsError(AppException):
    """Raised when a visa type already exists."""

    def __init__(self, field: str, value: str):
        super().__init__(
            f"Visa type with {field} '{value}' already exists."
        )


class VisaTypeNotFoundError(AppException):
    """Raised when a visa type is not found."""

    def __init__(self, visa_type_id: int):
        super().__init__(
            f"Visa type with ID {visa_type_id} not found."
        )