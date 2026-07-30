from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.administration.api_client import APIClient


class ClientIPWhitelist(BaseModel):
    """Client IP Whitelist model."""

    __tablename__ = "client_ip_whitelists"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("api_clients.id"),
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    cidr_range: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    api_client: Mapped["APIClient"] = relationship(
        "APIClient",
        back_populates="client_ip_whitelists",
    )