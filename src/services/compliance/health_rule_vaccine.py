from sqlalchemy.orm import Session

from src.exceptions.compliance.health_rule_vaccine import (
    HealthRuleVaccineAlreadyExistsError,
    HealthRuleVaccineNotFoundError,
)
from src.models.compliance.health_rule_vaccine import (
    HealthRuleVaccine,
)
from src.repositories.compliance.health_rule_vaccine import (
    HealthRuleVaccineRepository,
)
from src.schemas.compliance.health_rule_vaccine import (
    HealthRuleVaccineCreate,
    HealthRuleVaccineUpdate,
)
from src.services.base_crud_service import (
    BaseCrudService,
)


class HealthRuleVaccineService:
    """Service layer for HealthRuleVaccine business logic."""

    def __init__(
        self,
        health_rule_vaccine_repository: (
            HealthRuleVaccineRepository
        ),
    ) -> None:
        self.health_rule_vaccine_repository = (
            health_rule_vaccine_repository
        )
        self.crud = BaseCrudService(
            health_rule_vaccine_repository,
        )

    def create_health_rule_vaccine(
        self,
        db: Session,
        health_rule_vaccine_data: (
            HealthRuleVaccineCreate
        ),
    ) -> HealthRuleVaccine:
        """Create a new health rule vaccine."""

        if (
            self.health_rule_vaccine_repository.get_by_health_rule_and_vaccine(
                db,
                health_rule_vaccine_data.health_rule_id,
                health_rule_vaccine_data.vaccine_id,
            )
            is not None
        ):
            raise (
                HealthRuleVaccineAlreadyExistsError(
                    health_rule_id=health_rule_vaccine_data.health_rule_id,
                    vaccine_id=health_rule_vaccine_data.vaccine_id,
                )
            )

        return self.crud.create(
            db=db,
            model=HealthRuleVaccine,
            data=health_rule_vaccine_data,
        )

    def get_health_rule_vaccine(
        self,
        db: Session,
        health_rule_vaccine_id: int,
    ) -> HealthRuleVaccine:
        """Retrieve a health rule vaccine by ID."""

        health_rule_vaccine = self.crud.get_by_id(
            db=db,
            obj_id=health_rule_vaccine_id,
        )

        if health_rule_vaccine is None:
            raise (
                HealthRuleVaccineNotFoundError(
                    health_rule_vaccine_id,
                )
            )

        return health_rule_vaccine

    def get_all_health_rule_vaccines(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[HealthRuleVaccine]:
        """Retrieve all health rule vaccines."""


        return self.crud.get_all(db, skip, limit)

    def update_health_rule_vaccine(
        self,
        db: Session,
        health_rule_vaccine_id: int,
        health_rule_vaccine_data: (
            HealthRuleVaccineUpdate
        ),
    ) -> HealthRuleVaccine:
        """Update an existing health rule vaccine."""

        health_rule_vaccine = (
            self.get_health_rule_vaccine(
                db=db,
                health_rule_vaccine_id=health_rule_vaccine_id,
            )
        )

        update_data = (
            health_rule_vaccine_data.model_dump(
                exclude_unset=True,
            )
        )

        health_rule_id = update_data.get(
            "health_rule_id",
            health_rule_vaccine.health_rule_id,
        )

        vaccine_id = update_data.get(
            "vaccine_id",
            health_rule_vaccine.vaccine_id,
        )

        if (
            health_rule_id
            != health_rule_vaccine.health_rule_id
            or vaccine_id
            != health_rule_vaccine.vaccine_id
        ):
            existing = (
                self.health_rule_vaccine_repository.get_by_health_rule_and_vaccine(
                    db,
                    health_rule_id,
                    vaccine_id,
                )
            )

            if (
                existing is not None
                and existing.id
                != health_rule_vaccine.id
            ):
                raise (
                    HealthRuleVaccineAlreadyExistsError(
                        health_rule_id=health_rule_id,
                        vaccine_id=vaccine_id,
                    )
                )

        return self.crud.update(
            db=db,
            obj=health_rule_vaccine,
            data=health_rule_vaccine_data,
        )

    def delete_health_rule_vaccine(
        self,
        db: Session,
        health_rule_vaccine_id: int,
    ) -> None:
        """Delete a health rule vaccine."""

        health_rule_vaccine = (
            self.get_health_rule_vaccine(
                db=db,
                health_rule_vaccine_id=health_rule_vaccine_id,
            )
        )

        self.crud.delete(
            db=db,
            obj=health_rule_vaccine,
        )