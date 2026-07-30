from src.exceptions.base import AppException


class RuleHistoryNotFoundError(AppException):
    """Raised when a rule history record cannot be found."""

    def __init__(
        self,
        history_id: int,
    ):
        self.history_id = history_id

        super().__init__(
            f"Rule history with id {history_id} was not found."
        )