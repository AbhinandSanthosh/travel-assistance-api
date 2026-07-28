from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.health_rule_vaccine import (
        HealthRuleVaccine,
    )


class Vaccine(BaseModel):
    """Master data for vaccines."""

    __tablename__ = "vaccines"

    vaccine_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    disease: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    health_rule_vaccines: Mapped[
        list["HealthRuleVaccine"]
    ] = relationship(
        back_populates="vaccine",
    )