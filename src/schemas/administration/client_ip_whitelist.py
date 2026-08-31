from pydantic import ConfigDict

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class ClientIPWhitelistBase(StrictInputSchema):
    """Base schema for Client IP Whitelist."""

    client_id: int
    ip_address: str | None = None
    cidr_range: str | None = None
    description: str | None = None
    is_primary: bool = False
    active: bool = True


class ClientIPWhitelistCreate(ClientIPWhitelistBase):
    """Schema for creating a Client IP Whitelist."""
    pass


class ClientIPWhitelistUpdate(StrictInputSchema):
    """Schema for updating a Client IP Whitelist."""

    client_id: int | None = None
    ip_address: str | None = None
    cidr_range: str | None = None
    description: str | None = None
    is_primary: bool | None = None
    active: bool | None = None


class ClientIPWhitelistResponse(
    ClientIPWhitelistBase,
    BaseResponseSchema,
):
    """Schema for Client IP Whitelist response."""

    model_config = ConfigDict(from_attributes=True)