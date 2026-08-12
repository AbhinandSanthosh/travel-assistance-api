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

    # Legacy plaintext key column. Nullable now -- new clients created
    # through the self-service portal (see client_portal_service.py)
    # never populate this; they only get api_key_hash below. Kept
    # around (read-only, never written to for new signups) so
    # already-seeded/demo clients from before the portal existed keep
    # working. See AutoCheckService._validate_api_key for the fallback
    # lookup.
    api_key: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # --- Self-service client portal fields ---

    # bcrypt hash of the portal login password. NULL until the client
    # completes signup (mirrors User.password_hash / hash_password()).
    contact_password_hash: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # SHA-256 hex digest of the current live API key. NULL until the
    # client generates one from the portal. See src/core/api_key.py
    # for why this is SHA-256 (fast, deterministic lookup) rather than
    # bcrypt (slow, salted, made for low-entropy human passwords).
    api_key_hash: Mapped[str | None] = mapped_column(
        Text,
        unique=True,
        nullable=True,
    )

    # Short, safe-to-display fragments of the current key, e.g.
    # prefix="tac_live_9f3a", last_four="52b1" -> shown in the
    # dashboard as "tac_live_9f3a...52b1". The full key itself is
    # never stored or retrievable after generation.
    api_key_prefix: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    api_key_last_four: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    api_key_created_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    api_key_revoked_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    contact_name: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    contact_email: Mapped[str] = mapped_column(
        unique=True,
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