from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.compliance.rule import Rule
    from src.models.reference.country import Country
    from src.models.reference.passport_type import PassportType
    from src.models.reference.purpose import Purpose
    from src.models.reference.travel_authorization import (
        TravelAuthorization,
    )


class TravelAuthorizationRule(BaseModel):
    __tablename__ = "travel_authorization_rules"

    rule_id: Mapped[int] = mapped_column(
        ForeignKey(
            "rules.id",
            name="fk_travel_authorization_rules_rule_id",
        ),
        unique=True,
        nullable=False,
    )

    authorization_id: Mapped[int] = mapped_column(
        ForeignKey(
            "travel_authorizations.id",
            name="fk_travel_authorization_rules_authorization_id",
        ),
        nullable=False,
    )

    nationality_country_id: Mapped[int] = mapped_column(
        ForeignKey(
            "countries.id",
            name="fk_travel_authorization_rules_nationality_country_id",
        ),
        nullable=False,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey(
            "countries.id",
            name="fk_travel_authorization_rules_destination_country_id",
        ),
        nullable=False,
    )

    passport_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            "passport_types.id",
            name="fk_travel_authorization_rules_passport_type_id",
        ),
        nullable=False,
    )

    purpose_id: Mapped[int] = mapped_column(
        ForeignKey(
            "purposes.id",
            name="fk_travel_authorization_rules_purpose_id",
        ),
        nullable=False,
    )

    authorization_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    validity_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
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
        back_populates="travel_authorization_rule",
    )

    authorization: Mapped["TravelAuthorization"] = relationship(
        "TravelAuthorization",
        back_populates="travel_authorization_rule",
    )

    nationality_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[nationality_country_id],
        back_populates="travel_authorization_nationality_rules",
    )

    destination_country: Mapped["Country"] = relationship(
        "Country",
        foreign_keys=[destination_country_id],
        back_populates="travel_authorization_destination_rules",
    )

    passport_type: Mapped["PassportType"] = relationship(
        "PassportType",
        back_populates="travel_authorization_rules",
    )

    purpose: Mapped["Purpose"] = relationship(
        "Purpose",
        back_populates="travel_authorization_rules",
    )