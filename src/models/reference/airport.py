from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from .country import Country
    from src.models.compliance.transit_rule import TransitRule
    from src.models.reference.city import City


class Airport(BaseModel):
    __tablename__ = "airports"

    iata_code: Mapped[str | None] = mapped_column(
        String(3),
        unique=True,
        nullable=True,
    )

    icao_code: Mapped[str | None] = mapped_column(
        String(4),
        unique=True,
        nullable=True,
    )

    airport_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey(
            "countries.id",
            name="fk_airports_country_id",
        ),
        nullable=False,
    )

    timezone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    international: Mapped[bool] = mapped_column(
        Boolean,
        server_default="true",
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="airports",
    )

    transit_rules: Mapped[list["TransitRule"]] = relationship(
        "TransitRule",
        back_populates="transit_airport",
    )

    city_id: Mapped[int | None] = mapped_column(
        ForeignKey("cities.id", name="fk_airports_city_id"),
        nullable=True,  # flip to False once backfilled
    )

    city: Mapped["City | None"] = relationship(
        "City",
        back_populates="airports",
    )