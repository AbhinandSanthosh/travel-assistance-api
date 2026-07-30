from enum import Enum


class CollectionType(str, Enum):
    """Collection type enum."""

    MANUAL = "MANUAL"
    API = "API"
    CRAWLER = "CRAWLER"