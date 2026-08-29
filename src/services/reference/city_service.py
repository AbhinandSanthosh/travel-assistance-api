from sqlalchemy.orm import Session

from src.exceptions.reference.city import (
    CityAlreadyExistsError,
    CityNotFoundError,
)
from src.exceptions.reference.country import CountryNotFoundError
from src.models.reference.city import City
from src.repositories.reference.city_repository import (
    CityRepository,
)
from src.repositories.reference.country_repository import (
    CountryRepository,
)
from src.schemas.reference.city import (
    CityCreate,
    CityUpdate,
)
from src.services.base_crud_service import BaseCrudService


class CityService:
    """Service layer for City."""

    def __init__(
        self,
        city_repository: CityRepository,
        country_repository: CountryRepository,
    ):
        self.city_repository = city_repository
        self.country_repository = country_repository
        self.base_crud = BaseCrudService(
            city_repository,
        )

    def create_city(
        self,
        db: Session,
        city_data: CityCreate,
    ) -> City:
        """Create a new city."""

        existing_code = self.city_repository.get_by_city_code(
            db,
            city_data.city_code,
        )
        if existing_code:
            raise CityAlreadyExistsError(
                "city_code",
                city_data.city_code,
            )

        country = self.country_repository.get_by_id(
            db,
            city_data.country_id,
        )

        if not country:
            raise CountryNotFoundError(
                city_data.country_id,
            )

        return self.base_crud.create(
            db=db,
            model=City,
            data=city_data,
        )

    def get_city(
        self,
        db: Session,
        city_id: int,
    ) -> City:
        """Get a city by ID."""

        city = self.base_crud.get_by_id(
            db=db,
            obj_id=city_id,
        )

        if not city:
            raise CityNotFoundError(
                city_id,
            )

        return city

    def get_all_cities(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[City]:
        """Get all cities."""


        return self.base_crud.get_all(db, skip, limit)

    def update_city(
        self,
        db: Session,
        city_id: int,
        city_data: CityUpdate,
    ) -> City:
        """Update a city."""

        city = self.base_crud.get_by_id(
            db=db,
            obj_id=city_id,
        )

        if not city:
            raise CityNotFoundError(
                city_id,
            )

        update_data = city_data.model_dump(
            exclude_unset=True,
        )

        if (
            "city_code" in update_data
            and update_data["city_code"] != city.city_code
            and update_data["city_code"] is not None
        ):
            existing = self.city_repository.get_by_city_code(
                db,
                update_data["city_code"],
            )

            if existing:
                raise CityAlreadyExistsError(
                    "city_code",
                    update_data["city_code"],
                )

        if (
            "country_id" in update_data
            and update_data["country_id"] != city.country_id
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
            obj=city,
            data=city_data,
        )

    def delete_city(
        self,
        db: Session,
        city_id: int,
    ) -> None:
        """Delete a city."""

        city = self.base_crud.get_by_id(
            db=db,
            obj_id=city_id,
        )

        if not city:
            raise CityNotFoundError(
                city_id,
            )

        self.base_crud.delete(
            db=db,
            obj=city,
        )