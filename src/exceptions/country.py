from src.exceptions.base import AppException


class CountryAlreadyExistsError(AppException):
    """Raised when a country already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Country with {field} '{value}' already exists.")


class CountryNotFoundError(AppException):
    """Raised when a country cannot be found."""

    def __init__(self, country_id: int):
        self.country_id = country_id
        super().__init__(f"Country with id {country_id} was not found.")