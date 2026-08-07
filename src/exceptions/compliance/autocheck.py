from src.exceptions.base import AppException


class InvalidAPIKeyError(AppException):
    """Raised when the supplied API key does not match any registered client."""

    def __init__(self) -> None:
        super().__init__(
            message="Invalid or unknown API key.",
            code="AUTOCHECK_INVALID_API_KEY",
            status_code=401,
        )


class UnknownReferenceDataError(AppException):
    """Raised when nationality, destination, purpose, or passport type
    cannot be resolved against reference/master data."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            message=detail,
            code="AUTOCHECK_UNKNOWN_REFERENCE_DATA",
            status_code=400,
        )


class ClientInactiveError(AppException):
    """Raised when the API client has been deactivated."""

    def __init__(self) -> None:
        super().__init__(
            message="This API client is inactive.",
            code="AUTOCHECK_CLIENT_INACTIVE",
            status_code=403,
        )


class ClientExpiredError(AppException):
    """Raised when the API client's access has expired."""

    def __init__(self, expired_at: str) -> None:
        super().__init__(
            message=f"This API client's access expired on {expired_at}.",
            code="AUTOCHECK_CLIENT_EXPIRED",
            status_code=403,
        )


class IPNotWhitelistedError(AppException):
    """Raised when the caller's IP is not on the client's whitelist."""

    def __init__(self, ip_address: str) -> None:
        super().__init__(
            message=f"IP address {ip_address} is not authorized for this client.",
            code="AUTOCHECK_IP_NOT_WHITELISTED",
            status_code=403,
        )


class RateLimitExceededError(AppException):
    """Raised when the client has exceeded its requests-per-minute limit."""

    def __init__(self, requests_per_minute: int) -> None:
        super().__init__(
            message=(
                f"Rate limit exceeded: this client is limited to "
                f"{requests_per_minute} requests per minute."
            ),
            code="AUTOCHECK_RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


class NoApplicableRulesError(AppException):
    """Raised when no compliance rules of any kind are configured yet
    for the requested nationality/destination pair."""

    def __init__(self, nationality: str, destination: str) -> None:
        super().__init__(
            message=(
                f"No compliance rules are configured for travellers from "
                f"{nationality} to {destination} yet."
            ),
            code="AUTOCHECK_NO_APPLICABLE_RULES",
            status_code=404,
        )