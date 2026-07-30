from src.exceptions.base import AppException


class DocumentVersionFileHashAlreadyExistsError(AppException):
    """Raised when a document version file hash already exists."""

    def __init__(self, file_hash: str):
        super().__init__(
            f"Document version with file hash '{file_hash}' already exists."
        )


class DocumentVersionAlreadyExistsError(AppException):
    """Raised when a document version already exists."""

    def __init__(
        self,
        document_id: int,
        version_number: str,
    ):
        super().__init__(
            f"Document version '{version_number}' already exists for document id {document_id}."
        )


class DocumentVersionNotFoundError(AppException):
    """Raised when a document version is not found."""

    def __init__(self, document_version_id: int):
        super().__init__(
            f"Document version with id {document_version_id} was not found."
        )