from sqlalchemy.orm import Session

from src.exceptions.country import (
    CountryAlreadyExistsError,
    CountryNotFoundError,
)
from src.models.reference.country import Country
from src.repositories.reference.country_repository import CountryRepository
from src.schemas.reference.country import (
    CountryCreate,
    CountryUpdate,
)

from src.repositories.reference.region_repository import RegionRepository
from src.repositories.reference.currency_repository import CurrencyRepository

from src.exceptions.region import RegionNotFoundError
from src.exceptions.currency import CurrencyNotFoundError

class CountryService:
    """Service layer for Country business logic."""

    def __init__(
        self,
        country_repository: CountryRepository,
        region_repository: RegionRepository,
        currency_repository: CurrencyRepository,
    ):
        self.country_repository = country_repository
        self.region_repository = region_repository
        self.currency_repository = currency_repository

    def create_country(
        self,
        db: Session,
        country_data: CountryCreate,
    ) -> Country:
        """Create a new country."""

        if self.country_repository.get_by_iso2(db, country_data.iso2) is not None:
            raise CountryAlreadyExistsError(
                field="iso2",
                value=country_data.iso2,
            )

        if self.country_repository.get_by_iso3(db, country_data.iso3) is not None:
            raise CountryAlreadyExistsError(
                field="iso3",
                value=country_data.iso3,
            )

        region = self.region_repository.get_by_id(
            db,
            country_data.region_id,
        )

        if not region:
            raise RegionNotFoundError(country_data.region_id)

        currency = self.currency_repository.get_by_id(
            db,
            country_data.currency_id,
        )

        if not currency:
            raise CurrencyNotFoundError(country_data.currency_id)

        country = Country(**country_data.model_dump())

        return self.country_repository.create(
            db=db,
            obj=country,
        )

    def get_country(
        self,
        db: Session,
        country_id: int,
    ) -> Country:
        """Retrieve a country by ID."""

        country = self.country_repository.get_by_id(
            db=db,
            obj_id=country_id,
        )

        if country is None:
            raise CountryNotFoundError(country_id)

        return country

    def get_all_countries(
        self,
        db: Session,
    ) -> list[Country]:
        """Retrieve all countries."""

        return self.country_repository.get_all(db)

    def update_country(
        self,
        db: Session,
        country_id: int,
        country_data: CountryUpdate,
    ) -> Country:
        """Update an existing country."""

        country = self.get_country(
            db=db,
            country_id=country_id,
        )

        update_data = country_data.model_dump(exclude_unset=True)

        if "iso2" in update_data and update_data["iso2"] != country.iso2:
            existing = self.country_repository.get_by_iso2(
                db,
                update_data["iso2"],
            )

            if existing is not None:
                raise CountryAlreadyExistsError(
                    field="iso2",
                    value=update_data["iso2"],
                )

        if "iso3" in update_data and update_data["iso3"] != country.iso3:
            existing = self.country_repository.get_by_iso3(
                db,
                update_data["iso3"],
            )

            if existing is not None:
                raise CountryAlreadyExistsError(
                    field="iso3",
                    value=update_data["iso3"],
                )

        for field, value in update_data.items():
            setattr(country, field, value)

        return self.country_repository.save(
            db=db,
            obj=country,
        )

    def delete_country(
        self,
        db: Session,
        country_id: int,
    ) -> None:
        """Delete a country."""

        country = self.get_country(
            db=db,
            country_id=country_id,
        )

        self.country_repository.delete(
            db=db,
            obj=country,
        )