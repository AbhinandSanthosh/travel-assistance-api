from sqlalchemy.orm import Session

from src.models.reference.airport import Airport
from src.repositories.base_repository import BaseRepository


class AirportRepository(BaseRepository[Airport]):
    """Repository for Airport operations."""

    def __init__(self):
        super().__init__(Airport)

    def get_by_iata_code(
        self,
        db: Session,
        iata_code: str,
    ) -> Airport | None:
        """Retrieve an airport by IATA code."""

        return (
            db.query(Airport)
            .filter(Airport.iata_code == iata_code)
            .first()
        )

    def get_by_icao_code(
        self,
        db: Session,
        icao_code: str,
    ) -> Airport | None:
        """Retrieve an airport by ICAO code."""

        return (
            db.query(Airport)
            .filter(Airport.icao_code == icao_code)
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        airport_name: str,
    ) -> Airport | None:
        """Retrieve an airport by name."""

        return (
            db.query(Airport)
            .filter(Airport.airport_name == airport_name)
            .first()
        )