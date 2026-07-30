from typing import TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.visa_rule import VisaRule
    from src.models.compliance.travel_authorization_rule import TravelAuthorizationRule

class Purpose(BaseModel):
    __tablename__ = "purposes"

    purpose_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    purpose_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    visa_rules: Mapped[list["VisaRule"]] = relationship(
        "VisaRule",
        back_populates="purpose",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    travel_authorization_rules: Mapped[list["TravelAuthorizationRule"]] = relationship(
        "TravelAuthorizationRule",
        back_populates="purpose",
    )