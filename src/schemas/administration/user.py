from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas.common import BaseResponseSchema


class UserBase(BaseModel):
    """Shared fields for User schemas."""

    username: str = Field(
        ...,
        max_length=100,
    )

    full_name: str = Field(
        ...,
        max_length=150,
    )

    email: EmailStr

    role_id: int

    phone: str | None = Field(
        default=None,
        max_length=30,
    )


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(
        ...,
        min_length=8,
    )


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str | None = Field(
        default=None,
        max_length=100,
    )

    full_name: str | None = Field(
        default=None,
        max_length=150,
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
    )

    role_id: int | None = None

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    status: bool | None = None

    last_login: datetime | None = None


class UserResponse(BaseResponseSchema):
    """Schema returned for user responses."""

    username: str
    full_name: str
    email: EmailStr
    role_id: int
    phone: str | None
    status: bool
    last_login: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )