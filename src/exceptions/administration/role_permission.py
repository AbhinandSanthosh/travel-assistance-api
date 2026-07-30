from src.exceptions.base import AppException


class RolePermissionAlreadyExistsError(AppException):
    """Raised when a role-permission mapping already exists."""

    def __init__(self, role_id: int, permission_id: int):
        self.role_id = role_id
        self.permission_id = permission_id
        super().__init__(
            f"RolePermission mapping already exists for role id "
            f"{role_id} and permission id {permission_id}."
        )


class RolePermissionNotFoundError(AppException):
    """Raised when a role-permission mapping cannot be found."""

    def __init__(self, role_permission_id: int):
        self.role_permission_id = role_permission_id
        super().__init__(
            f"RolePermission with id {role_permission_id} was not found."
        )