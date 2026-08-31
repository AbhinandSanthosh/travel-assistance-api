from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, field_validator

from src.core.security import password_policy_errors
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class UserBase(StrictInputSchema):
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

    @field_validator("password")
    @classmethod
    def _check_password_policy(cls, value: str) -> str:
        errors = password_policy_errors(value)
        if errors:
            raise ValueError("Password does not meet policy: " + "; ".join(errors))
        return value


class UserUpdate(StrictInputSchema):
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

    @field_validator("password")
    @classmethod
    def _check_password_policy(cls, value: str | None) -> str | None:
        if value is None:
            return value
        errors = password_policy_errors(value)
        if errors:
            raise ValueError("Password does not meet policy: " + "; ".join(errors))
        return value

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