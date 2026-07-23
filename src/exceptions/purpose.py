from src.exceptions.base import AppException


class PurposeAlreadyExistsError(AppException):
    """Raised when a purpose already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ):
        self.field = field
        self.value = value
        super().__init__(
            f"Purpose with {field} '{value}' already exists."
        )


class PurposeNotFoundError(AppException):
    """Raised when a purpose cannot be found."""

    def __init__(
        self,
        purpose_id: int,
    ):
        self.purpose_id = purpose_id
        super().__init__(
            f"Purpose with id {purpose_id} was not found."
        )