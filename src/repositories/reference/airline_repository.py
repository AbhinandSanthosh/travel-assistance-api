from sqlalchemy.orm import Session

from src.models.reference.airline import Airline
from src.repositories.base_repository import BaseRepository


class AirlineRepository(BaseRepository[Airline]):
    """Repository for Airline operations."""

    def __init__(self):
        super().__init__(Airline)

    def get_by_iata_code(
        self,
        db: Session,
        iata_code: str,
    ) -> Airline | None:
        """Retrieve an airline by IATA code."""

        return (
            db.query(Airline)
            .filter(Airline.iata_code == iata_code)
            .first()
        )

    def get_by_icao_code(
        self,
        db: Session,
        icao_code: str,
    ) -> Airline | None:
        """Retrieve an airline by ICAO code."""

        return (
            db.query(Airline)
            .filter(Airline.icao_code == icao_code)
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        airline_name: str,
    ) -> Airline | None:
        """Retrieve an airline by name."""

        return (
            db.query(Airline)
            .filter(Airline.airline_name == airline_name)
            .first()
        )