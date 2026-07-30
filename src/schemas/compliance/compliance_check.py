from typing import Any

from pydantic import BaseModel, ConfigDict

from src.enums.decision import Decision
from src.schemas.common import BaseResponseSchema


class ComplianceCheckBase(BaseModel):
    """Base schema for compliance check."""

    request_id: str
    client_id: int
    input_hash: str
    rule_version_id: int
    decision: Decision
    decision_reasons: list[dict[str, Any]] | None = None
    response_json: dict[str, Any]


class ComplianceCheckCreate(
    ComplianceCheckBase,
):
    """Schema for creating a compliance check."""


class ComplianceCheckUpdate(BaseModel):
    """Schema for updating a compliance check."""

    request_id: str | None = None
    client_id: int | None = None
    input_hash: str | None = None
    rule_version_id: int | None = None
    decision: Decision | None = None
    decision_reasons: (
        list[dict[str, Any]] | None
    ) = None
    response_json: (
        dict[str, Any] | None
    ) = None


class ComplianceCheckResponse(
    BaseResponseSchema,
    ComplianceCheckBase,
):
    """Schema for compliance check response."""

    model_config = ConfigDict(
        from_attributes=True,
    )