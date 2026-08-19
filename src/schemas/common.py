from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StrictInputSchema(BaseModel):
    """Base for every admin-writable (Create/Update) request schema.

    extra="forbid" rejects any field in the request body that isn't
    declared on the schema, instead of silently dropping it. Without
    this, a malformed or malicious payload with an unexpected field
    name (e.g. a typo, or a field renamed in a later API version)
    passes validation with the extra data quietly discarded -- which
    for a compliance rule payload means a caller can believe a value
    was written when it wasn't, with no error to tell them otherwise.
    """

    model_config = ConfigDict(extra="forbid")


class TimestampSchema(BaseModel):
    """Common timestamp fields shared across response schemas."""

    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(TimestampSchema):
    """Base response schema with the primary key."""

    id: int


