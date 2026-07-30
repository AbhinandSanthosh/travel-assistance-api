from src.exceptions.base import AppException


class ClientIPWhitelistNotFoundError(AppException):
    """Raised when a client IP whitelist entry cannot be found."""

    def __init__(
        self,
        whitelist_id: int,
    ):
        self.whitelist_id = whitelist_id

        super().__init__(
            f"Client IP whitelist entry with id {whitelist_id} was not found."
        )


class InvalidWhitelistEntryError(AppException):
    """Raised when both IP address and CIDR range are missing."""

    def __init__(self):
        super().__init__(
            "Either ip_address or cidr_range must be provided."
        )