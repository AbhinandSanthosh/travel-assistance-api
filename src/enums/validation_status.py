from enum import Enum


class ValidationStatus(str, Enum):
    """Validation status enum."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"