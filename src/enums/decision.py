from enum import Enum


class Decision(str, Enum):
    """Compliance decision enum."""

    ALLOWED = "ALLOWED"
    CONDITIONAL = "CONDITIONAL"
    NOT_ALLOWED = "NOT_ALLOWED"