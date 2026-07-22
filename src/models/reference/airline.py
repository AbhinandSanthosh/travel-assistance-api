from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from .country import Country


class Airline(BaseModel):
    __tablename__ = "airlines"

    airline_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    iata_code: Mapped[str | None] = mapped_column(
        String(2),
        unique=True,
        nullable=True,
    )

    icao_code: Mapped[str | None] = mapped_column(
        String(3),
        unique=True,
        nullable=True,
    )

    country_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "countries.id",
            name="fk_airlines_country_id",
        ),
        nullable=False,
    )

    country: Mapped["Country | None"] = relationship(
        "Country",
        back_populates="airlines",
    )