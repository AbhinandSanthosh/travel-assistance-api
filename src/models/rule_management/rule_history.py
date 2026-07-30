from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel
from src.enums.change_type import ChangeType

if TYPE_CHECKING:
    from src.models.administration.user import User
    from src.models.compliance.rule import Rule
    from src.models.rule_management.rule_version import RuleVersion


class RuleHistory(BaseModel):
    """Rule History model."""

    __tablename__ = "rule_histories"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        nullable=False,
    )

    previous_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("rule_versions.id"),
        nullable=True,
    )

    new_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("rule_versions.id"),
        nullable=True,
    )

    change_type: Mapped[ChangeType] = mapped_column(
        Enum(ChangeType, name="change_type_enum"),
        nullable=False,
    )

    change_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    # ---------------- Relationships ---------------- #

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="rule_history",
    )

    previous_version: Mapped["RuleVersion | None"] = relationship(
        "RuleVersion",
        foreign_keys=[previous_version_id],
        back_populates="previous_version_histories",
    )

    new_version: Mapped["RuleVersion | None"] = relationship(
        "RuleVersion",
        foreign_keys=[new_version_id],
        back_populates="new_version_histories",
    )

    changed_by_user: Mapped["User | None"] = relationship(
        "User",
        back_populates="rule_histories",
    )