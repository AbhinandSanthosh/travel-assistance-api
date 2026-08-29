from sqlalchemy.orm import Session

from src.exceptions.reference.country import (
    CountryAlreadyExistsError,
    CountryNotFoundError,
)
from src.exceptions.reference.currency import CurrencyNotFoundError
from src.exceptions.reference.region import RegionNotFoundError

from src.models.reference.country import Country

from src.repositories.reference.country_repository import CountryRepository
from src.repositories.reference.currency_repository import CurrencyRepository
from src.repositories.reference.region_repository import RegionRepository

from src.schemas.reference.country import (
    CountryCreate,
    CountryUpdate,
)

from src.services.base_crud_service import BaseCrudService

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
        self.base_crud = BaseCrudService(country_repository)

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

        return self.base_crud.create(
            db=db,
            model=Country,
            data=country_data,
        )

    def get_country(
        self,
        db: Session,
        country_id: int,
    ) -> Country:
        """Retrieve a country by ID."""

        country = self.base_crud.get_by_id(
        db=db,
        obj_id=country_id,
        )

        if country is None:
            raise CountryNotFoundError(country_id)

        return country

    def get_all_countries(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Country]:
        """Retrieve all countries."""


        return self.base_crud.get_all(db, skip, limit)
    
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

        update_data = country_data.model_dump(
            exclude_unset=True,
        )

        if (
            "iso2" in update_data
            and update_data["iso2"] != country.iso2
        ):
            existing = self.country_repository.get_by_iso2(
                db,
                update_data["iso2"],
            )

            if existing is not None:
                raise CountryAlreadyExistsError(
                    field="iso2",
                    value=update_data["iso2"],
                )

        if (
            "iso3" in update_data
            and update_data["iso3"] != country.iso3
        ):
            existing = self.country_repository.get_by_iso3(
                db,
                update_data["iso3"],
            )

            if existing is not None:
                raise CountryAlreadyExistsError(
                    field="iso3",
                    value=update_data["iso3"],
                )

        if (
            "region_id" in update_data
            and update_data["region_id"] != country.region_id
        ):
            region = self.region_repository.get_by_id(
                db,
                update_data["region_id"],
            )

            if not region:
                raise RegionNotFoundError(
                    update_data["region_id"],
                )

        if (
            "currency_id" in update_data
            and update_data["currency_id"] != country.currency_id
        ):
            currency = self.currency_repository.get_by_id(
                db,
                update_data["currency_id"],
            )

            if not currency:
                raise CurrencyNotFoundError(
                    update_data["currency_id"],
                )

        return self.base_crud.update(
            db=db,
            obj=country,
            data=country_data,
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

        self.base_crud.delete(
            db=db,
            obj=country,
        )