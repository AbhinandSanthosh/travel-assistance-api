from pydantic import BaseModel, ConfigDict

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RolePermissionBase(StrictInputSchema):
    """Shared fields for RolePermission schemas."""

    role_id: int
    permission_id: int


class RolePermissionCreate(RolePermissionBase):
    """Schema for creating a role-permission mapping."""

    pass


class RolePermissionUpdate(StrictInputSchema):
    """Schema for updating a role-permission mapping."""

    role_id: int | None = None
    permission_id: int | None = None


class RolePermissionResponse(
    BaseResponseSchema,
    RolePermissionBase,
):
    """Schema returned for role-permission responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )