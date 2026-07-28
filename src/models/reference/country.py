from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.reference.region import Region
    from src.models.reference.currency import Currency
    from .travel_authorization import TravelAuthorization
    from .airline import Airline
    from .airport import Airport
    from src.models.compliance.visa_rule import VisaRule
    from src.models.compliance.passport_rule import PassportRule


class Country(BaseModel):
    __tablename__ = "countries"

    iso2: Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False,
    )

    iso3: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
    )

    country_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    nationality: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id"),
        nullable=False,
    )

    capital: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
    )

    official_language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    timezone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    region: Mapped["Region"] = relationship(
        "Region",
        back_populates="countries",
    )

    currency: Mapped["Currency"] = relationship(
        "Currency",
        back_populates="countries",
    )

    travel_authorizations: Mapped[list["TravelAuthorization"]] = relationship(
    "TravelAuthorization",
    back_populates="destination_country",
    )

    airlines: Mapped[list["Airline"]] = relationship(
    "Airline",
    back_populates="country",
    )

    airports: Mapped[list["Airport"]] = relationship(
    "Airport",
    back_populates="country",
    )

    nationality_visa_rules: Mapped[list["VisaRule"]] = relationship(
        "VisaRule",
        foreign_keys="VisaRule.nationality_country_id",
        back_populates="nationality_country",
    )

    destination_visa_rules: Mapped[list["VisaRule"]] = relationship(
        "VisaRule",
        foreign_keys="VisaRule.destination_country_id",
        back_populates="destination_country",
    )

    destination_passport_rules: Mapped[list["PassportRule"]] = relationship(
        "PassportRule",
        back_populates="destination_country",
    )

