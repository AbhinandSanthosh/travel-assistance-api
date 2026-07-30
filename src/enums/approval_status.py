from enum import Enum


class ApprovalStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"