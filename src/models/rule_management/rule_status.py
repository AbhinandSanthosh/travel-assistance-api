from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule


class RuleStatus(BaseModel):
    """Rule Status model."""

    __tablename__ = "rule_statuses"

    status_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    status_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    rules: Mapped[list["Rule"]] = relationship(
        "Rule",
        back_populates="status",
    )