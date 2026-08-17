from sqlalchemy.orm import Session

from src.models.reference.city import City
from src.repositories.base_repository import BaseRepository


class CityRepository(BaseRepository[City]):
    """Repository for City operations."""

    def __init__(self):
        super().__init__(City)

    def get_by_city_code(
        self,
        db: Session,
        city_code: str,
    ) -> City | None:
        """Retrieve a city by IATA city code."""

        return (
            db.query(City)
            .filter(City.city_code == city_code)
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        city_name: str,
    ) -> City | None:
        """Retrieve a city by name."""

        return (
            db.query(City)
            .filter(City.city_name == city_name)
            .first()
        )