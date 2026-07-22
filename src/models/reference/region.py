from sqlalchemy import String, Text

from src.db.base_model import BaseModel
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.reference.country import Country

class Region(BaseModel):
    __tablename__ = "regions"

    region_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    countries: Mapped[list["Country"]] = relationship(
        "Country",
        back_populates="region",
    )