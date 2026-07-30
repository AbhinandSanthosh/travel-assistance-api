from enum import Enum


class ExtractionStatus(str, Enum):
    """Extraction status enum."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"