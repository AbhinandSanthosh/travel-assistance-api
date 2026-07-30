from datetime import date

from src.exceptions.base import AppException


class ClientUsageStatisticsNotFoundError(AppException):
    """Raised when client usage statistics cannot be found."""

    def __init__(self, statistics_id: int):
        super().__init__(
            f"Client usage statistics with id {statistics_id} was not found."
        )


class ClientUsageStatisticsAlreadyExistsError(AppException):
    """Raised when statistics already exist for a client and date."""

    def __init__(
        self,
        client_id: int,
        usage_date: date,
    ):
        super().__init__(
            f"Usage statistics already exist for client {client_id} on {usage_date}."
        )