from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.administration.api_client import APIClient


class ClientUsageStatistics(BaseModel):
    """Client Usage Statistics model."""

    __tablename__ = "client_usage_statistics"

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "usage_date",
            name="uq_client_usage_date",
        ),
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("api_clients.id"),
        nullable=False,
    )

    usage_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    total_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    successful_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    failed_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    average_response_time: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    api_client: Mapped["APIClient"] = relationship(
        "APIClient",
        back_populates="client_usage_statistics",
    )