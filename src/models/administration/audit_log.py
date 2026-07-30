from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.audit_action import AuditAction

if TYPE_CHECKING:
    from src.models.administration.user import User


class AuditLog(BaseModel):
    """Audit Log model."""

    __tablename__ = "audit_logs"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    entity_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(AuditAction),
        nullable=False,
    )

    old_value: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    new_value: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="audit_logs",
    )