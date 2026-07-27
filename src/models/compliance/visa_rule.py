from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.reference.passport_type import PassportType
    from src.models.reference.purpose import Purpose
    from src.models.reference.visa_type import VisaType


class VisaRule(BaseModel):
    __tablename__ = "visa_rules"

    __table_args__ = (
        Index(
            "ix_visa_rules_nationality_destination",
            "nationality_country_id",
            "destination_country_id",
        ),
        Index(
            "ix_visa_rules_passport_type",
            "passport_type_id",
        ),
        Index(
            "ix_visa_rules_purpose",
            "purpose_id",
        ),
    )

    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.id"),
        unique=True,
        nullable=False,
    )

    nationality_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    passport_type_id: Mapped[int] = mapped_column(
        ForeignKey("passport_types.id"),
        nullable=False,
    )

    visa_type_id: Mapped[int] = mapped_column(
        ForeignKey("visa_types.id"),
        nullable=False,
    )

    purpose_id: Mapped[int] = mapped_column(
        ForeignKey("purposes.id"),
        nullable=False,
    )

    visa_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    visa_on_arrival: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    evisa_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    max_stay_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    multiple_entry: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    condition_expression: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    exemption_expression: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rule: Mapped["Rule"] = relationship(
        "Rule",
        back_populates="visa_rules",
    )

    nationality_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[nationality_country_id],
        back_populates="nationality_visa_rules",
    )

    destination_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[destination_country_id],
        back_populates="destination_visa_rules",
    )

    passport_type: Mapped["PassportType"] = relationship(
        "PassportType",
        back_populates="visa_rules",
    )

    visa_type: Mapped["VisaType"] = relationship(
        "VisaType",
        back_populates="visa_rules",
    )

    purpose: Mapped["Purpose"] = relationship(
        "Purpose",
        back_populates="visa_rules",
    )