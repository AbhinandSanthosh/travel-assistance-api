from src.exceptions.base import AppException


class VaccineAlreadyExistsError(
    AppException,
):
    """Raised when a vaccine already exists."""

    def __init__(
        self,
        field: str,
        value: str,
    ) -> None:
        self.field = field
        self.value = value

        super().__init__(
            f"Vaccine with {field} "
            f"'{value}' already exists."
        )


class VaccineNotFoundError(
    AppException,
):
    """Raised when a vaccine cannot be found."""

    def __init__(
        self,
        vaccine_id: int,
    ) -> None:
        self.vaccine_id = vaccine_id

        super().__init__(
            "Vaccine with id "
            f"{vaccine_id} "
            "was not found."
        )