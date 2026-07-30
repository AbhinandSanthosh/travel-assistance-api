from enum import Enum


class AuditAction(str, Enum):
    """Supported audit log actions."""

    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"