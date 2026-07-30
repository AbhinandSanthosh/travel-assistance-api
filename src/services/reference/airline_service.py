from sqlalchemy.orm import Session

from src.exceptions.reference.airline import (
    AirlineAlreadyExistsError,
    AirlineNotFoundError,
)
from src.exceptions.reference.country import CountryNotFoundError
from src.models.reference.airline import Airline
from src.repositories.reference.airline_repository import (
    AirlineRepository,
)
from src.repositories.reference.country_repository import (
    CountryRepository,
)
from src.schemas.reference.airline import (
    AirlineCreate,
    AirlineUpdate,
)

from src.services.base_crud_service import BaseCrudService

class AirlineService:
    """Service layer for Airline."""
    def __init__(
        self,
        airline_repository: AirlineRepository,
        country_repository: CountryRepository,
    ):
        self.airline_repository = airline_repository
        self.country_repository = country_repository
        self.base_crud = BaseCrudService(airline_repository)

    def create_airline(
        self,
        db: Session,
        airline_data: AirlineCreate,
    ) -> Airline:
        """Create a new airline."""

        existing_name = self.airline_repository.get_by_name(
            db,
            airline_data.airline_name,
        )
        if existing_name:
            raise AirlineAlreadyExistsError(
                "airline_name",
                airline_data.airline_name,
            )

        if airline_data.iata_code:
            existing_iata = (
                self.airline_repository.get_by_iata_code(
                    db,
                    airline_data.iata_code,
                )
            )
            if existing_iata:
                raise AirlineAlreadyExistsError(
                    "iata_code",
                    airline_data.iata_code,
                )

        if airline_data.icao_code:
            existing_icao = (
                self.airline_repository.get_by_icao_code(
                    db,
                    airline_data.icao_code,
                )
            )
            if existing_icao:
                raise AirlineAlreadyExistsError(
                    "icao_code",
                    airline_data.icao_code,
                )

        country = self.country_repository.get_by_id(
            db,
            airline_data.country_id,
        )

        if not country:
            raise CountryNotFoundError(
                airline_data.country_id,
            )

        return self.base_crud.create(
            db=db,
            model=Airline,
            data=airline_data,
        )

    def get_airline(
        self,
        db: Session,
        airline_id: int,
    ) -> Airline:
        """Get an airline by ID."""

        airline = self.base_crud.get_by_id(
            db=db,
            obj_id=airline_id,
        )

        if not airline:
            raise AirlineNotFoundError(
                airline_id,
            )

        return airline

    def get_all_airlines(
        self,
        db: Session,
    ) -> list[Airline]:
        """Get all airlines."""

        return self.base_crud.get_all(db)

    def update_airline(
        self,
        db: Session,
        airline_id: int,
        airline_data: AirlineUpdate,
    ) -> Airline:
        """Update an airline."""

        airline = self.base_crud.get_by_id(
            db=db,
            obj_id=airline_id,
        )

        if not airline:
            raise AirlineNotFoundError(
                airline_id,
            )

        update_data = airline_data.model_dump(
            exclude_unset=True,
        )

        if (
            "airline_name" in update_data
            and update_data["airline_name"]
            != airline.airline_name
        ):
            existing = self.airline_repository.get_by_name(
                db,
                update_data["airline_name"],
            )
            if existing:
                raise AirlineAlreadyExistsError(
                    "airline_name",
                    update_data["airline_name"],
                )

        if (
            "iata_code" in update_data
            and update_data["iata_code"]
            != airline.iata_code
            and update_data["iata_code"] is not None
        ):
            existing = self.airline_repository.get_by_iata_code(
                db,
                update_data["iata_code"],
            )
            if existing:
                raise AirlineAlreadyExistsError(
                    "iata_code",
                    update_data["iata_code"],
                )

        if (
            "icao_code" in update_data
            and update_data["icao_code"]
            != airline.icao_code
            and update_data["icao_code"] is not None
        ):
            existing = self.airline_repository.get_by_icao_code(
                db,
                update_data["icao_code"],
            )
            if existing:
                raise AirlineAlreadyExistsError(
                    "icao_code",
                    update_data["icao_code"],
                )

        if (
            "country_id" in update_data
            and update_data["country_id"]
            != airline.country_id
        ):
            country = self.country_repository.get_by_id(
                db,
                update_data["country_id"],
            )

            if not country:
                raise CountryNotFoundError(
                    update_data["country_id"],
                )

        return self.base_crud.update(
            db=db,
            obj=airline,
            data=airline_data,
        )

    def delete_airline(
        self,
        db: Session,
        airline_id: int,
    ) -> None:
        """Delete an airline."""

        airline = self.base_crud.get_by_id(
            db=db,
            obj_id=airline_id,
        )

        if not airline:
            raise AirlineNotFoundError(
                airline_id,
            )

        self.base_crud.delete(
            db=db,
            obj=airline,
        )