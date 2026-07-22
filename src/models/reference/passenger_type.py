from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_model import BaseModel


class PassengerType(BaseModel):
    __tablename__ = "passenger_types"

    passenger_type_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    passenger_type_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )