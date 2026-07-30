from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.approval_status import ApprovalStatus

if TYPE_CHECKING:
    from src.models.administration.user import User
    from src.models.compliance.rule import Rule


class RuleApproval(BaseModel):
    """Rule Approval model."""

    __tablename__ = "rule_approvals"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    approval_status: Mapped[ApprovalStatus] = mapped_column(
        Enum(
            ApprovalStatus,
            name="approval_status_enum",
        ),
        nullable=False,
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="rule_approvals",
    )

    reviewer: Mapped["User"] = relationship(
        "User",
        back_populates="rule_approvals",
    )