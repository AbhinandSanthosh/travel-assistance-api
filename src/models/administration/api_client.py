from sqlalchemy import Boolean, Enum, Integer, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.subscription_plan import SubscriptionPlan
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.administration.client_ip_whitelist import (
        ClientIPWhitelist,
    )
    from src.models.administration.api_request_log import (
        APIRequestLog,
    )
    from src.models.administration.client_usage_statistics import (
        ClientUsageStatistics,
    )
    from src.models.compliance.compliance_check import ComplianceCheck

class APIClient(BaseModel):
    """API Client model."""

    __tablename__ = "api_clients"

    client_name: Mapped[str] = mapped_column(
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        nullable=False,
    )

    client_code: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )

    api_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    contact_name: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    contact_email: Mapped[str] = mapped_column(
        nullable=False,
    )

    contact_phone: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(
            SubscriptionPlan,
            name="subscription_plan_enum",
        ),
        nullable=False,
    )

    requests_per_minute: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    client_ip_whitelists: Mapped[list["ClientIPWhitelist"]] = relationship(
        "ClientIPWhitelist",
        back_populates="api_client",
    )

    api_request_logs: Mapped[list["APIRequestLog"]] = relationship(
        "APIRequestLog",
        back_populates="api_client",
    )

    client_usage_statistics: Mapped[list["ClientUsageStatistics"]] = relationship(
        "ClientUsageStatistics",
        back_populates="api_client",
    )

    compliance_checks: Mapped[list["ComplianceCheck"]] = relationship(
        "ComplianceCheck",
        back_populates="client",
    )