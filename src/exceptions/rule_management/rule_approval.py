from src.exceptions.base import AppException


class RuleApprovalAlreadyExistsError(AppException):
    """Raised when a reviewer has already reviewed the rule."""

    def __init__(
        self,
        rule_id: int,
        reviewer_id: int,
    ):
        self.rule_id = rule_id
        self.reviewer_id = reviewer_id

        super().__init__(
            f"Reviewer {reviewer_id} has already reviewed rule {rule_id}."
        )


class RuleApprovalNotFoundError(AppException):
    """Raised when a rule approval cannot be found."""

    def __init__(
        self,
        approval_id: int,
    ):
        self.approval_id = approval_id

        super().__init__(
            f"Rule approval with id {approval_id} was not found."
        )