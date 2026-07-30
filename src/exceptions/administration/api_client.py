from src.exceptions.base import AppException


class APIClientAlreadyExistsError(AppException):
    """Raised when an API client code already exists."""

    def __init__(
        self,
        client_code: str,
    ):
        self.client_code = client_code

        super().__init__(
            f"API client with code '{client_code}' already exists."
        )


class APIClientNotFoundError(AppException):
    """Raised when an API client cannot be found."""

    def __init__(
        self,
        client_id: int,
    ):
        self.client_id = client_id

        super().__init__(
            f"API client with id {client_id} was not found."
        )