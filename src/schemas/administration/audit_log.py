from pydantic import ConfigDict

from src.enums.audit_action import AuditAction
from src.schemas.common import BaseResponseSchema


class AuditLogBase(BaseResponseSchema):
    """Base schema for Audit Log."""

    user_id: int
    entity_name: str
    entity_id: int
    action: AuditAction
    old_value: dict | None = None
    new_value: dict | None = None
    ip_address: str | None = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an Audit Log."""

    pass


class AuditLogResponse(
    AuditLogBase,
    BaseResponseSchema,
):
    """Schema for Audit Log response."""

    model_config = ConfigDict(from_attributes=True)