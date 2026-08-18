from src.exceptions.base import AppException


class InvalidCredentialsError(AppException):
    """Raised when username or password is incorrect."""

    def __init__(self) -> None:
        super().__init__(
            message="Invalid username or password.",
            code="INVALID_CREDENTIALS",
            status_code=401,
        )


class InactiveUserError(AppException):
    """Raised when a user account exists but is deactivated."""

    def __init__(self) -> None:
        super().__init__(
            message="This user account is inactive.",
            code="USER_INACTIVE",
            status_code=403,
        )


class InvalidOrExpiredTokenError(AppException):
    """Raised when a Bearer JWT is missing, malformed, or expired."""

    def __init__(self) -> None:
        super().__init__(
            message=(
                "Invalid or expired authentication token. "
                "Please log in again."
            ),
            code="INVALID_TOKEN",
            status_code=401,
        )


class InsufficientPermissionsError(AppException):
    """Raised when an authenticated admin user lacks the
    required role/permission for an action."""

    def __init__(self) -> None:
        super().__init__(
            message="You do not have permission to perform this action.",
            code="INSUFFICIENT_PERMISSIONS",
            status_code=403,
        )


class TooManyLoginAttemptsError(AppException):
    """Raised when an IP exceeds the login rate limit."""

    def __init__(self, limit: int) -> None:
        super().__init__(
            message=(
                f"Too many login attempts. Limit is {limit} per minute. "
                "Please wait and try again."
            ),
            code="TOO_MANY_LOGIN_ATTEMPTS",
            status_code=429,
        )
