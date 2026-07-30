from src.exceptions.base import AppException


class SourceDocumentDocumentURLAlreadyExistsError(AppException):
    """Raised when a document URL already exists."""

    def __init__(self, document_url: str):
        super().__init__(
            f"Source document with URL '{document_url}' already exists."
        )


class SourceDocumentFileHashAlreadyExistsError(AppException):
    """Raised when a file hash already exists."""

    def __init__(self, file_hash: str):
        super().__init__(
            f"Source document with file hash '{file_hash}' already exists."
        )


class SourceDocumentNotFoundError(AppException):
    """Raised when a source document is not found."""

    def __init__(self, source_document_id: int):
        super().__init__(
            f"Source document with id {source_document_id} was not found."
        )