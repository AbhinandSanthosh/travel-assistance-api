from datetime import date

from pydantic import ConfigDict

from src.schemas.common import BaseResponseSchema, StrictInputSchema


class ClientUsageStatisticsBase(StrictInputSchema):
    """Base schema for Client Usage Statistics."""

    client_id: int
    usage_date: date
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: int | None = None


class ClientUsageStatisticsCreate(ClientUsageStatisticsBase):
    """Schema for creating client usage statistics."""

    pass


class ClientUsageStatisticsUpdate(StrictInputSchema):
    """Schema for updating client usage statistics."""

    total_requests: int | None = None
    successful_requests: int | None = None
    failed_requests: int | None = None
    average_response_time: int | None = None


class ClientUsageStatisticsResponse(
    ClientUsageStatisticsBase,
    BaseResponseSchema,
):
    """Schema for client usage statistics response."""

    model_config = ConfigDict(from_attributes=True)