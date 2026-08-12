from src.exceptions.base import AppException


class ClientAlreadyRegisteredError(AppException):
    """Raised when a portal signup is attempted for an email that
    already has an account."""

    def __init__(self, contact_email: str) -> None:
        self.contact_email = contact_email
        super().__init__(
            message=(
                f"An account already exists for '{contact_email}'. "
                "Log in instead."
            ),
            code="CLIENT_ALREADY_REGISTERED",
            status_code=409,
        )


class InvalidClientCredentialsError(AppException):
    """Raised when portal login email/password don't match."""

    def __init__(self) -> None:
        super().__init__(
            message="Invalid email or password.",
            code="INVALID_CLIENT_CREDENTIALS",
            status_code=401,
        )


class ClientPortalAccountInactiveError(AppException):
    """Raised when a portal account exists but is deactivated."""

    def __init__(self) -> None:
        super().__init__(
            message="This account is inactive. Contact support.",
            code="CLIENT_ACCOUNT_INACTIVE",
            status_code=403,
        )


class InvalidOrExpiredPortalTokenError(AppException):
    """Raised when a client-portal Bearer token is missing, malformed,
    expired, or was issued for a different token type (e.g. an admin
    JWT reused against a portal endpoint)."""

    def __init__(self) -> None:
        super().__init__(
            message="Invalid or expired session. Please log in again.",
            code="INVALID_PORTAL_TOKEN",
            status_code=401,
        )