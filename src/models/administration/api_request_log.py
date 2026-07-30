from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.http_method import HTTPMethod

if TYPE_CHECKING:
    from src.models.administration.api_client import APIClient


class APIRequestLog(BaseModel):
    """API Request Log model."""

    __tablename__ = "api_request_logs"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("api_clients.id"),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    endpoint: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    http_method: Mapped[HTTPMethod] = mapped_column(
        SQLEnum(HTTPMethod),
        nullable=False,
    )

    request_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    request_body: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    response_status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    response_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    api_client: Mapped["APIClient"] = relationship(
        "APIClient",
        back_populates="api_request_logs",
    )