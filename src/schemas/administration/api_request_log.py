from pydantic import BaseModel, ConfigDict

from src.enums.http_method import HTTPMethod
from src.schemas.common import BaseResponseSchema, StrictInputSchema


class APIRequestLogBase(StrictInputSchema):
    """Base schema for API Request Log."""

    client_id: int
    ip_address: str
    endpoint: str
    http_method: HTTPMethod
    request_id: str
    request_body: dict | None = None
    response_status: int
    response_time_ms: int


class APIRequestLogCreate(APIRequestLogBase):
    """Schema for creating an API Request Log."""

    pass


class APIRequestLogResponse(
    APIRequestLogBase,
    BaseResponseSchema,
):
    """Schema for API Request Log response."""

    model_config = ConfigDict(from_attributes=True)