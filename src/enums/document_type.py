from enum import Enum


class DocumentType(str, Enum):
    """Document type enum."""

    PDF = "PDF"
    HTML = "HTML"
    API_RESPONSE = "API_RESPONSE"