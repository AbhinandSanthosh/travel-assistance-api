from src.exceptions.base import AppException


class DocumentValidationNotFoundError(
    AppException,
):
    """Raised when a document validation is not found."""

    def __init__(self) -> None:
        super().__init__(
            message="Document Validation not found.",
            code="DOCUMENT_VALIDATION_NOT_FOUND",
            status_code=404,
        )