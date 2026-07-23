from sqlalchemy.orm import Session

from src.exceptions.airport import (
    AirportAlreadyExistsError,
    AirportNotFoundError,
)
from src.exceptions.country import CountryNotFoundError
from src.models.reference.airport import Airport
from src.repositories.reference.airport_repository import (
    AirportRepository,
)
from src.repositories.reference.country_repository import (
    CountryRepository,
)
from src.schemas.reference.airport import (
    AirportCreate,
    AirportUpdate,
)


class AirportService:
    """Service layer for Airport."""

    def __init__(
        self,
        airport_repository: AirportRepository,
        country_repository: CountryRepository,
    ):
        self.airport_repository = airport_repository
        self.country_repository = country_repository

    def create_airport(
        self,
        db: Session,
        airport_data: AirportCreate,
    ) -> Airport:
        """Create a new airport."""

        existing_name = self.airport_repository.get_by_name(
            db,
            airport_data.airport_name,
        )
        if existing_name:
            raise AirportAlreadyExistsError(
                "airport_name",
                airport_data.airport_name,
            )

        if airport_data.iata_code:
            existing_iata = self.airport_repository.get_by_iata_code(
                db,
                airport_data.iata_code,
            )
            if existing_iata:
                raise AirportAlreadyExistsError(
                    "iata_code",
                    airport_data.iata_code,
                )

        if airport_data.icao_code:
            existing_icao = self.airport_repository.get_by_icao_code(
                db,
                airport_data.icao_code,
            )
            if existing_icao:
                raise AirportAlreadyExistsError(
                    "icao_code",
                    airport_data.icao_code,
                )

        country = self.country_repository.get_by_id(
            db,
            airport_data.country_id,
        )
        if not country:
            raise CountryNotFoundError(
                airport_data.country_id,
            )

        airport = Airport(
            **airport_data.model_dump(),
        )

        return self.airport_repository.create(
            db,
            airport,
        )

    def get_airport(
        self,
        db: Session,
        airport_id: int,
    ) -> Airport:
        """Get an airport by ID."""

        airport = self.airport_repository.get_by_id(
            db,
            airport_id,
        )

        if not airport:
            raise AirportNotFoundError(
                airport_id,
            )

        return airport

    def get_all_airports(
        self,
        db: Session,
    ) -> list[Airport]:
        """Get all airports."""

        return self.airport_repository.get_all(
            db,
        )

    def update_airport(
        self,
        db: Session,
        airport_id: int,
        airport_data: AirportUpdate,
    ) -> Airport:
        """Update an airport."""

        airport = self.airport_repository.get_by_id(
            db,
            airport_id,
        )

        if not airport:
            raise AirportNotFoundError(
                airport_id,
            )

        update_data = airport_data.model_dump(
            exclude_unset=True,
        )

        if (
            "airport_name" in update_data
            and update_data["airport_name"]
            != airport.airport_name
        ):
            existing = self.airport_repository.get_by_name(
                db,
                update_data["airport_name"],
            )
            if existing:
                raise AirportAlreadyExistsError(
                    "airport_name",
                    update_data["airport_name"],
                )

        if (
            "iata_code" in update_data
            and update_data["iata_code"]
            != airport.iata_code
            and update_data["iata_code"] is not None
        ):
            existing = self.airport_repository.get_by_iata_code(
                db,
                update_data["iata_code"],
            )
            if existing:
                raise AirportAlreadyExistsError(
                    "iata_code",
                    update_data["iata_code"],
                )

        if (
            "icao_code" in update_data
            and update_data["icao_code"]
            != airport.icao_code
            and update_data["icao_code"] is not None
        ):
            existing = self.airport_repository.get_by_icao_code(
                db,
                update_data["icao_code"],
            )
            if existing:
                raise AirportAlreadyExistsError(
                    "icao_code",
                    update_data["icao_code"],
                )

        if (
            "country_id" in update_data
            and update_data["country_id"]
            != airport.country_id
        ):
            country = self.country_repository.get_by_id(
                db,
                update_data["country_id"],
            )
            if not country:
                raise CountryNotFoundError(
                    update_data["country_id"],
                )

        for field, value in update_data.items():
            setattr(
                airport,
                field,
                value,
            )

        return self.airport_repository.save(
            db,
            airport,
        )

    def delete_airport(
        self,
        db: Session,
        airport_id: int,
    ) -> None:
        """Delete an airport."""

        airport = self.airport_repository.get_by_id(
            db,
            airport_id,
        )

        if not airport:
            raise AirportNotFoundError(
                airport_id,
            )

        self.airport_repository.delete(
            db,
            airport,
        )