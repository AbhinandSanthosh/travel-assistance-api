from sqlalchemy.orm import Session

from src.exceptions.compliance.entry_restriction import (
    EntryRestrictionAlreadyExistsError,
    EntryRestrictionNotFoundError,
)
from src.models.compliance.entry_restriction import (
    EntryRestriction,
)
from src.repositories.compliance.entry_restriction import (
    EntryRestrictionRepository,
)
from src.schemas.compliance.entry_restriction import (
    EntryRestrictionCreate,
    EntryRestrictionUpdate,
)
from src.services.base_crud_service import (
    BaseCrudService,
)


class EntryRestrictionService:
    """Service layer for EntryRestriction business logic."""

    def __init__(
        self,
        entry_restriction_repository: EntryRestrictionRepository,
    ) -> None:
        self.entry_restriction_repository = (
            entry_restriction_repository
        )
        self.crud = BaseCrudService(
            entry_restriction_repository,
        )

    def create_entry_restriction(
        self,
        db: Session,
        entry_restriction_data: EntryRestrictionCreate,
    ) -> EntryRestriction:
        """Create a new entry restriction."""

        if (
            self.entry_restriction_repository.get_by_rule_id(
                db,
                entry_restriction_data.rule_id,
            )
            is not None
        ):
            raise EntryRestrictionAlreadyExistsError(
                field="rule_id",
                value=entry_restriction_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=EntryRestriction,
            data=entry_restriction_data,
        )

    def get_entry_restriction(
        self,
        db: Session,
        entry_restriction_id: int,
    ) -> EntryRestriction:
        """Retrieve an entry restriction by ID."""

        entry_restriction = self.crud.get_by_id(
            db=db,
            obj_id=entry_restriction_id,
        )

        if entry_restriction is None:
            raise EntryRestrictionNotFoundError(
                entry_restriction_id,
            )

        return entry_restriction

    def get_all_entry_restrictions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[EntryRestriction]:
        """Retrieve all entry restrictions."""


        return self.crud.get_all(db, skip, limit)

    def update_entry_restriction(
        self,
        db: Session,
        entry_restriction_id: int,
        entry_restriction_data: EntryRestrictionUpdate,
    ) -> EntryRestriction:
        """Update an existing entry restriction."""

        entry_restriction = self.get_entry_restriction(
            db=db,
            entry_restriction_id=entry_restriction_id,
        )

        update_data = (
            entry_restriction_data.model_dump(
                exclude_unset=True,
            )
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != entry_restriction.rule_id
        ):
            existing = (
                self.entry_restriction_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise EntryRestrictionAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=entry_restriction,
            data=entry_restriction_data,
        )

    def delete_entry_restriction(
        self,
        db: Session,
        entry_restriction_id: int,
    ) -> None:
        """Delete an entry restriction."""

        entry_restriction = self.get_entry_restriction(
            db=db,
            entry_restriction_id=entry_restriction_id,
        )

        self.crud.delete(
            db=db,
            obj=entry_restriction,
        )