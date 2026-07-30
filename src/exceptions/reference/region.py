from src.exceptions.base import AppException


class RegionAlreadyExistsError(AppException):
    """Raised when a region with the given name already exists."""

    def __init__(self, region_name: str):
        super().__init__(f"Region '{region_name}' already exists.")


class RegionNotFoundError(AppException):
    """Raised when a region is not found."""

    def __init__(self, region_id: int):
        super().__init__(f"Region with ID {region_id} not found.")