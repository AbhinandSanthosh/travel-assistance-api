from enum import Enum


class ChangeType(str, Enum):
    """Supported rule history change types."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PUBLISH = "PUBLISH"
    EXPIRE = "EXPIRE"