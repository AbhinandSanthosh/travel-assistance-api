from src.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    """Raised when a user already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value

        super().__init__(
            f"User with {field} '{value}' already exists."
        )


class UserNotFoundError(AppException):
    """Raised when a user cannot be found."""

    def __init__(
        self,
        user_id: int,
    ):
        self.user_id = user_id

        super().__init__(
            f"User with id {user_id} was not found."
        )