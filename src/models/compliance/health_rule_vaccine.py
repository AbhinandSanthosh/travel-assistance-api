from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.health_rule import HealthRule
    from src.models.compliance.vaccine import Vaccine
    from src.models.administration.user import User


class HealthRuleVaccine(
    BaseModel,
):
    """Association between health rules and vaccines."""

    __tablename__ = "health_rule_vaccines"

    health_rule_id: Mapped[int] = mapped_column(
        ForeignKey("health_rules.id"),
        nullable=False,
    )

    vaccine_id: Mapped[int] = mapped_column(
        ForeignKey("vaccines.id"),
        nullable=False,
    )

    certificate_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    health_rule: Mapped["HealthRule"] = relationship(
        back_populates="health_rule_vaccines",
    )

    vaccine: Mapped["Vaccine"] = relationship(
        back_populates="health_rule_vaccines",
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    updated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_by_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_health_rule_vaccines",
    )

    updated_by_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[updated_by],
        back_populates="updated_health_rule_vaccines",
    )