from src.exceptions.base import AppException


class CityAlreadyExistsError(AppException):
    """Raised when a city already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"City with {field} '{value}' already exists."
        )


class CityNotFoundError(AppException):
    """Raised when a city cannot be found."""

    def __init__(
        self,
        city_id: int,
    ):
        self.city_id = city_id
        super().__init__(
            f"City with id {city_id} was not found."
        )