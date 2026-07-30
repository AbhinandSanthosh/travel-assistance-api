from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.decision import Decision

if TYPE_CHECKING:
    from src.models.administration.api_client import APIClient
    from src.models.rule_management.rule_version import RuleVersion


class ComplianceCheck(BaseModel):
    """Compliance Check model."""

    __tablename__ = "compliance_checks"

    request_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("api_clients.id"),
        nullable=False,
    )

    input_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    rule_version_id: Mapped[int] = mapped_column(
        ForeignKey("rule_versions.id"),
        nullable=False,
    )

    decision: Mapped[Decision] = mapped_column(
        SQLEnum(Decision),
        nullable=False,
    )

    decision_reasons: Mapped[
        list[dict[str, Any]] | None
    ] = mapped_column(
        JSONB,
        nullable=True,
    )

    response_json: Mapped[
        dict[str, Any]
    ] = mapped_column(
        JSONB,
        nullable=False,
    )

    client: Mapped["APIClient"] = relationship(
        "APIClient",
    )

    rule_version: Mapped["RuleVersion"] = relationship(
        "RuleVersion",
    )