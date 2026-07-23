from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.reference.currency import Currency
from src.repositories.base_repository import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    """Repository for Currency model."""

    def __init__(self):
        super().__init__(Currency)

    def get_by_code(
        self,
        db: Session,
        currency_code: str,
    ) -> Currency | None:
        """Get a currency by its ISO code."""
        stmt = select(Currency).where(
            Currency.currency_code == currency_code,
        )
        return db.scalar(stmt)

    def get_by_name(
        self,
        db: Session,
        currency_name: str,
    ) -> Currency | None:
        """Get a currency by its name."""
        stmt = select(Currency).where(
            Currency.currency_name == currency_name,
        )
        return db.scalar(stmt)