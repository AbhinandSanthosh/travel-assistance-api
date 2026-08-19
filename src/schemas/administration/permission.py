from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class PermissionBase(StrictInputSchema):
    """Shared fields for Permission schemas."""

    permission_code: str = Field(
        ...,
        max_length=100,
    )

    permission_name: str = Field(
        ...,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
    )


class PermissionCreate(PermissionBase):
    """Schema for creating a permission."""

    pass


class PermissionUpdate(StrictInputSchema):
    """Schema for updating a permission."""

    permission_code: str | None = Field(
        default=None,
        max_length=100,
    )

    permission_name: str | None = Field(
        default=None,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
    )


class PermissionResponse(
    BaseResponseSchema,
    PermissionBase,
):
    """Schema returned for permission responses."""

    model_config = ConfigDict(
        from_attributes=True,
    )