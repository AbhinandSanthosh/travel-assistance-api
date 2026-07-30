from src.exceptions.base import AppException


class CurrencyAlreadyExistsError(AppException):
    """Raised when a currency already exists."""

    def __init__(self, field: str, value: str):
        super().__init__(f"Currency with {field} '{value}' already exists.")


class CurrencyNotFoundError(AppException):
    """Raised when a currency is not found."""

    def __init__(self, currency_id: int):
        super().__init__(f"Currency with ID {currency_id} not found.")