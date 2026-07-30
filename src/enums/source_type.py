from enum import Enum


class SourceType(str, Enum):
    API = "API"
    WEBSITE = "WEBSITE"
    PDF = "PDF"
    EMAIL = "EMAIL"