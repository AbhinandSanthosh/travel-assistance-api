from enum import Enum


class CollectionStatus(str, Enum):
    """Collection status enum."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"