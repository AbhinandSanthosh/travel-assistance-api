from sqlalchemy import String

from src.db.base_model import BaseModel
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.models.reference.country import Country
    from src.models.compliance.customs_rule import CustomsRule

class Currency(BaseModel):
    __tablename__ = "currencies"

    currency_code: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
    )

    currency_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    currency_symbol: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    countries: Mapped[list["Country"]] = relationship(
        "Country",
        back_populates="currency",
    )

    customs_rules: Mapped[
        list["CustomsRule"]
    ] = relationship(
        back_populates="currency",
    )

