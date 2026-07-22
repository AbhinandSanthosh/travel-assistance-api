from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .country import Country

class TravelAuthorization(BaseModel):
    __tablename__ = "travel_authorizations"

    authorization_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    authorization_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    destination_country_id: Mapped[int] = mapped_column(
        ForeignKey(
            "countries.id",
            name="fk_travel_authorizations_destination_country_id",
        ),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    destination_country: Mapped["Country"] = relationship(
        "Country",
        back_populates="travel_authorizations",
    )