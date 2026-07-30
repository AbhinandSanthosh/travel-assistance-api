from src.exceptions.base import AppException


class ComplianceCheckRequestIdAlreadyExistsError(
    AppException,
):
    """Raised when the request ID already exists."""

    def __init__(self) -> None:
        super().__init__(
            message=(
                "Compliance Check with this "
                "request ID already exists."
            ),
            code=(
                "COMPLIANCE_CHECK_REQUEST_ID_ALREADY_EXISTS"
            ),
            status_code=400,
        )


class ComplianceCheckNotFoundError(
    AppException,
):
    """Raised when a compliance check is not found."""

    def __init__(self) -> None:
        super().__init__(
            message="Compliance Check not found.",
            code="COMPLIANCE_CHECK_NOT_FOUND",
            status_code=404,
        )