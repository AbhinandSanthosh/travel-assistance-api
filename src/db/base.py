from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover them
from src.models.reference import *  # noqa: E402,F401