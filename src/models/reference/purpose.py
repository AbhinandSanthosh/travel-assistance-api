from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_model import BaseModel


class Purpose(BaseModel):
    __tablename__ = "purposes"

    purpose_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    purpose_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )