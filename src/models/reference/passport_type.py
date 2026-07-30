from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.compliance.visa_rule import VisaRule
    from src.models.compliance.passport_rule import PassportRule
    from src.models.compliance.travel_authorization_rule import TravelAuthorizationRule

class PassportType(BaseModel):
    __tablename__ = "passport_types"

    passport_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    passport_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    visa_rules: Mapped[list["VisaRule"]] = relationship(
        "VisaRule",
        back_populates="passport_type",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    passport_rules: Mapped[list["PassportRule"]] = relationship(
        "PassportRule",
        back_populates="passport_type",
    )

    travel_authorization_rules: Mapped[list["TravelAuthorizationRule"]] = relationship(
        "TravelAuthorizationRule",
        back_populates="passport_type",
    )