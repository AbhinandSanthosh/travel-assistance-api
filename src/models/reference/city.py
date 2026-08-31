from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

if TYPE_CHECKING:
    from .country import Country
    from .airport import Airport


class City(BaseModel):
    __tablename__ = "cities"

    city_code: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
    )

    city_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id", name="fk_cities_country_id"),
        nullable=False,
    )

    timezone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped["Country"] = relationship(
        "Country",
        back_populates="cities",
    )

    airports: Mapped[list["Airport"]] = relationship(
        "Airport",
        back_populates="city_ref",
    )