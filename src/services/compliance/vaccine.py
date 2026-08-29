from sqlalchemy.orm import Session

from src.exceptions.compliance.vaccine import (
    VaccineAlreadyExistsError,
    VaccineNotFoundError,
)
from src.models.compliance.vaccine import Vaccine
from src.repositories.compliance.vaccine import (
    VaccineRepository,
)
from src.schemas.compliance.vaccine import (
    VaccineCreate,
    VaccineUpdate,
)
from src.services.base_crud_service import BaseCrudService


class VaccineService:
    """Service layer for Vaccine business logic."""

    def __init__(
        self,
        vaccine_repository: VaccineRepository,
    ) -> None:
        self.vaccine_repository = (
            vaccine_repository
        )
        self.crud = BaseCrudService(
            vaccine_repository,
        )

    def create_vaccine(
        self,
        db: Session,
        vaccine_data: VaccineCreate,
    ) -> Vaccine:
        """Create a new vaccine."""

        if (
            self.vaccine_repository.get_by_vaccine_name(
                db,
                vaccine_data.vaccine_name,
            )
            is not None
        ):
            raise VaccineAlreadyExistsError(
                field="vaccine_name",
                value=vaccine_data.vaccine_name,
            )

        return self.crud.create(
            db=db,
            model=Vaccine,
            data=vaccine_data,
        )

    def get_vaccine(
        self,
        db: Session,
        vaccine_id: int,
    ) -> Vaccine:
        """Retrieve a vaccine by ID."""

        vaccine = self.crud.get_by_id(
            db=db,
            obj_id=vaccine_id,
        )

        if vaccine is None:
            raise VaccineNotFoundError(
                vaccine_id,
            )

        return vaccine

    def get_all_vaccines(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Vaccine]:
        """Retrieve all vaccines."""


        return self.crud.get_all(db, skip, limit)

    def update_vaccine(
        self,
        db: Session,
        vaccine_id: int,
        vaccine_data: VaccineUpdate,
    ) -> Vaccine:
        """Update an existing vaccine."""

        vaccine = self.get_vaccine(
            db=db,
            vaccine_id=vaccine_id,
        )

        update_data = vaccine_data.model_dump(
            exclude_unset=True,
        )

        if (
            "vaccine_name" in update_data
            and update_data["vaccine_name"]
            != vaccine.vaccine_name
        ):
            existing = (
                self.vaccine_repository.get_by_vaccine_name(
                    db,
                    update_data["vaccine_name"],
                )
            )

            if existing is not None:
                raise VaccineAlreadyExistsError(
                    field="vaccine_name",
                    value=update_data["vaccine_name"],
                )

        return self.crud.update(
            db=db,
            obj=vaccine,
            data=vaccine_data,
        )

    def delete_vaccine(
        self,
        db: Session,
        vaccine_id: int,
    ) -> None:
        """Delete a vaccine."""

        vaccine = self.get_vaccine(
            db=db,
            vaccine_id=vaccine_id,
        )

        self.crud.delete(
            db=db,
            obj=vaccine,
        )