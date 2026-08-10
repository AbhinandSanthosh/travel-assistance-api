from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    """POST /api/v1/auth/login request body."""

    username: str = Field(..., examples=["admin@example.com"])
    password: str = Field(..., examples=["********"])


class LoginResponse(BaseModel):
    """POST /api/v1/auth/login success response.

    Field names are camelCase to match the published API spec
    (accessToken / tokenType / expiresIn).
    """

    access_token: str = Field(..., serialization_alias="accessToken")
    token_type: str = Field(
        default="Bearer",
        serialization_alias="tokenType",
    )
    expires_in: int = Field(..., serialization_alias="expiresIn")

    model_config = ConfigDict(populate_by_name=True)


class CurrentUserResponse(BaseModel):
    """GET /api/v1/auth/me response."""

    id: int
    username: str
    full_name: str
    email: str
    role_id: int
    role_name: str

    model_config = ConfigDict(from_attributes=True)
