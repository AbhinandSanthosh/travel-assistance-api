from src.exceptions.base import AppException


class SourceRegistryAuthorityNameAlreadyExistsError(AppException):
    """Raised when an authority name already exists."""

    def __init__(self, authority_name: str):
        self.authority_name = authority_name
        super().__init__(
            f"Source Registry with authority name '{authority_name}' already exists."
        )


class SourceRegistryWebsiteAlreadyExistsError(AppException):
    """Raised when a website already exists."""

    def __init__(self, website: str):
        self.website = website
        super().__init__(
            f"Source Registry with website '{website}' already exists."
        )


class SourceRegistryNotFoundError(AppException):
    """Raised when a source registry cannot be found."""

    def __init__(self, source_registry_id: int):
        self.source_registry_id = source_registry_id
        super().__init__(
            f"Source Registry with id {source_registry_id} was not found."
        )