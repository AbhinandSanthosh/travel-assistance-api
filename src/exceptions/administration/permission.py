from src.exceptions.base import AppException


class PermissionAlreadyExistsError(AppException):
    """Raised when a permission already exists."""

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(
            f"Permission with {field} '{value}' already exists."
        )


class PermissionNotFoundError(AppException):
    """Raised when a permission cannot be found."""

    def __init__(self, permission_id: int):
        self.permission_id = permission_id
        super().__init__(
            f"Permission with id {permission_id} was not found."
        )