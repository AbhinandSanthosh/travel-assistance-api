from sqlalchemy.orm import Session

from src.exceptions.rule_management.rule_version import (
    RuleVersionAlreadyExistsError,
    RuleVersionNotFoundError,
)
from src.models.rule_management.rule_version import RuleVersion
from src.repositories.rule_management.rule_version import (
    RuleVersionRepository,
)
from src.schemas.rule_management.rule_version import (
    RuleVersionCreate,
    RuleVersionUpdate,
)
from src.services.base_crud_service import BaseCrudService


class RuleVersionService:
    """Service layer for Rule Version business logic."""

    def __init__(
        self,
        rule_version_repository: RuleVersionRepository,
    ) -> None:
        self.rule_version_repository = rule_version_repository
        self.base_crud = BaseCrudService(rule_version_repository)

    def create_rule_version(
        self,
        db: Session,
        rule_version_data: RuleVersionCreate,
    ) -> RuleVersion:
        """Create a new rule version."""

        existing = self.rule_version_repository.get_by_rule_and_version(
            db=db,
            rule_id=rule_version_data.rule_id,
            version_number=rule_version_data.version_number,
        )

        if existing is not None:
            raise RuleVersionAlreadyExistsError(
                rule_id=rule_version_data.rule_id,
                version_number=rule_version_data.version_number,
            )

        return self.base_crud.create(
            db=db,
            model=RuleVersion,
            data=rule_version_data,
        )

    def get_rule_version(
        self,
        db: Session,
        rule_version_id: int,
    ) -> RuleVersion:
        """Retrieve a rule version by ID."""

        rule_version = self.base_crud.get_by_id(
            db=db,
            obj_id=rule_version_id,
        )

        if rule_version is None:
            raise RuleVersionNotFoundError(
                rule_version_id,
            )

        return rule_version

    def get_all_rule_versions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RuleVersion]:
        """Retrieve all rule versions."""


        return self.base_crud.get_all(db, skip, limit)

    def update_rule_version(
        self,
        db: Session,
        rule_version_id: int,
        rule_version_data: RuleVersionUpdate,
    ) -> RuleVersion:
        """Update an existing rule version."""

        rule_version = self.get_rule_version(
            db=db,
            rule_version_id=rule_version_id,
        )

        update_data = rule_version_data.model_dump(
            exclude_unset=True,
        )

        if (
            "version_number" in update_data
            and update_data["version_number"] != rule_version.version_number
        ):
            existing = self.rule_version_repository.get_by_rule_and_version(
                db=db,
                rule_id=rule_version.rule_id,
                version_number=update_data["version_number"],
            )

            if existing is not None:
                raise RuleVersionAlreadyExistsError(
                    rule_id=rule_version.rule_id,
                    version_number=update_data["version_number"],
                )

        return self.base_crud.update(
            db=db,
            obj=rule_version,
            data=rule_version_data,
        )

    def delete_rule_version(
        self,
        db: Session,
        rule_version_id: int,
    ) -> None:
        """Delete a rule version."""

        rule_version = self.get_rule_version(
            db=db,
            rule_version_id=rule_version_id,
        )

        self.base_crud.delete(
            db=db,
            obj=rule_version,
        )