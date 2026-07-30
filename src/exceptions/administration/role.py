from src.exceptions.base import AppException


class RoleAlreadyExistsError(AppException):
    """Raised when a role already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(
            f"Role with {field} '{value}' already exists."
        )


class RoleNotFoundError(AppException):
    """Raised when a role cannot be found."""

    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(
            f"Role with id {role_id} was not found."
        )