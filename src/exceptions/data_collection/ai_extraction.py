from src.exceptions.base import AppException


class AIExtractionNotFoundError(
    AppException,
):
    """Raised when an AI extraction is not found."""

    def __init__(self) -> None:
        super().__init__(
            message="AI Extraction not found.",
            code="AI_EXTRACTION_NOT_FOUND",
            status_code=404,
        )