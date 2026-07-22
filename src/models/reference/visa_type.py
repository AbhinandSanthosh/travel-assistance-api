from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_model import BaseModel


class VisaType(BaseModel):
    __tablename__ = "visa_types"

    visa_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    visa_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )