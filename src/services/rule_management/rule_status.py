from sqlalchemy.orm import Session

from src.exceptions.rule_management.rule_status import (
    RuleStatusAlreadyExistsError,
    RuleStatusNotFoundError,
)

from src.models.rule_management.rule_status import RuleStatus

from src.repositories.rule_management.rule_status import RuleStatusRepository

from src.schemas.rule_management.rule_status import (
    RuleStatusCreate,
    RuleStatusUpdate,
)

from src.services.base_crud_service import BaseCrudService


class RuleStatusService:
    """Service layer for Rule Status business logic."""

    def __init__(
        self,
        rule_status_repository: RuleStatusRepository,
    ):
        self.rule_status_repository = rule_status_repository
        self.base_crud = BaseCrudService(rule_status_repository)

    def create_rule_status(
        self,
        db: Session,
        rule_status_data: RuleStatusCreate,
    ) -> RuleStatus:
        """Create a new rule status."""

        existing = self.rule_status_repository.get_by_status_code(
            db,
            rule_status_data.status_code,
        )

        if existing is not None:
            raise RuleStatusAlreadyExistsError(
                field="status_code",
                value=rule_status_data.status_code,
            )

        return self.base_crud.create(
            db=db,
            model=RuleStatus,
            data=rule_status_data,
        )

    def get_rule_status(
        self,
        db: Session,
        rule_status_id: int,
    ) -> RuleStatus:
        """Retrieve a rule status by ID."""

        rule_status = self.base_crud.get_by_id(
            db=db,
            obj_id=rule_status_id,
        )

        if rule_status is None:
            raise RuleStatusNotFoundError(rule_status_id)

        return rule_status

    def get_all_rule_statuses(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RuleStatus]:
        """Retrieve all rule statuses."""


        return self.base_crud.get_all(db, skip, limit)

    def update_rule_status(
        self,
        db: Session,
        rule_status_id: int,
        rule_status_data: RuleStatusUpdate,
    ) -> RuleStatus:
        """Update an existing rule status."""

        rule_status = self.get_rule_status(
            db=db,
            rule_status_id=rule_status_id,
        )

        update_data = rule_status_data.model_dump(
            exclude_unset=True,
        )

        if (
            "status_code" in update_data
            and update_data["status_code"] != rule_status.status_code
        ):
            existing = self.rule_status_repository.get_by_status_code(
                db,
                update_data["status_code"],
            )

            if existing is not None:
                raise RuleStatusAlreadyExistsError(
                    field="status_code",
                    value=update_data["status_code"],
                )

        return self.base_crud.update(
            db=db,
            obj=rule_status,
            data=rule_status_data,
        )

    def delete_rule_status(
        self,
        db: Session,
        rule_status_id: int,
    ) -> None:
        """Delete a rule status."""

        rule_status = self.get_rule_status(
            db=db,
            rule_status_id=rule_status_id,
        )

        self.base_crud.delete(
            db=db,
            obj=rule_status,
        )