from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_model import BaseModel


class PassportType(BaseModel):
    __tablename__ = "passport_types"

    passport_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    passport_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )