from pydantic import ConfigDict, Field

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class RoleBase(StrictInputSchema):
    """Shared fields for Role schemas."""

    role_name: str = Field(
        ...,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
    )


class RoleCreate(RoleBase):
    """Schema for creating a role."""

    pass


class RoleUpdate(StrictInputSchema):
    """Schema for updating a role."""

    role_name: str | None = Field(
        default=None,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
    )


class RoleResponse(BaseResponseSchema, RoleBase):
    """Schema returned for role responses."""

    model_config = ConfigDict(from_attributes=True)