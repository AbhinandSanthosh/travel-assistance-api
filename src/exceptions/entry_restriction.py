from src.exceptions.base import AppException


class EntryRestrictionAlreadyExistsError(
    AppException,
):
    """Raised when an entry restriction already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Entry Restriction with {field} "
            f"'{value}' already exists."
        )


class EntryRestrictionNotFoundError(
    AppException,
):
    """Raised when an entry restriction cannot be found."""

    def __init__(
        self,
        entry_restriction_id: int,
    ) -> None:
        self.entry_restriction_id = (
            entry_restriction_id
        )

        super().__init__(
            "Entry Restriction with id "
            f"{entry_restriction_id} "
            "was not found."
        )