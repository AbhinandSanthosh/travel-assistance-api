from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from .role import Role
    from src.models.rule_management.rule_version import RuleVersion
    from src.models.rule_management.rule_history import RuleHistory
    from src.models.rule_management.rule_approval import RuleApproval
    from src.models.rule_management.rule_simulation import RuleSimulation
    from src.models.administration.audit_log import AuditLog


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
    )

    published_rule_versions: Mapped[list["RuleVersion"]] = relationship(
        "RuleVersion",
        back_populates="publisher",
    )

    rule_histories: Mapped[list["RuleHistory"]] = relationship(
        "RuleHistory",
        back_populates="changed_by_user",
    )

    rule_approvals: Mapped[list["RuleApproval"]] = relationship(
        "RuleApproval",
        back_populates="reviewer",
    )

    rule_simulations: Mapped[list["RuleSimulation"]] = relationship(
        "RuleSimulation",
        back_populates="executor",
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
    )