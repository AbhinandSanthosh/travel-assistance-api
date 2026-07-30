from src.exceptions.base import AppException


class APIRequestLogNotFoundError(AppException):
    """Raised when an API request log cannot be found."""

    def __init__(
        self,
        request_log_id: int,
    ):
        self.request_log_id = request_log_id

        super().__init__(
            f"API request log with id {request_log_id} was not found."
        )