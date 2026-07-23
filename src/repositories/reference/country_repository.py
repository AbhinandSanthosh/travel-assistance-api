from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.reference.country import Country
from src.repositories.base_repository import BaseRepository


class CountryRepository(BaseRepository[Country]):
    """Repository for Country-specific database operations."""

    def __init__(self) -> None:
        super().__init__(Country)

    def get_by_iso2(self, db: Session, iso2: str) -> Country | None:
        return db.scalar(
            select(Country).where(Country.iso2 == iso2)
        )

    def get_by_iso3(self, db: Session, iso3: str) -> Country | None:
        return db.scalar(
            select(Country).where(Country.iso3 == iso3)
        )

    def get_by_name(self, db: Session, country_name: str) -> Country | None:
        return db.scalar(
            select(Country).where(
                Country.country_name == country_name
            )
        )