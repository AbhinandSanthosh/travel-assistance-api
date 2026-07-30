from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule


class RuleExecutionLog(BaseModel):
    """Rule Execution Log model."""

    __tablename__ = "rule_execution_logs"

    request_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    matched: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    skipped: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    execution_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
    )