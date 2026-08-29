from sqlalchemy.orm import Session

from src.exceptions.compliance.passport_rule import (
    PassportRuleAlreadyExistsError,
    PassportRuleNotFoundError,
)
from src.models.compliance.passport_rule import PassportRule
from src.repositories.compliance.passport_rule import (
    PassportRuleRepository,
)
from src.schemas.compliance.passport_rule import (
    PassportRuleCreate,
    PassportRuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class PassportRuleService:
    """Service layer for PassportRule business logic."""

    def __init__(
        self,
        passport_rule_repository: PassportRuleRepository,
    ) -> None:
        self.passport_rule_repository = (
            passport_rule_repository
        )
        self.crud = BaseCrudService(
            passport_rule_repository,
        )

    def create_passport_rule(
        self,
        db: Session,
        passport_rule_data: PassportRuleCreate,
    ) -> PassportRule:
        """Create a new passport rule."""

        if (
            self.passport_rule_repository.get_by_rule_id(
                db,
                passport_rule_data.rule_id,
            )
            is not None
        ):
            raise PassportRuleAlreadyExistsError(
                field="rule_id",
                value=passport_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=PassportRule,
            data=passport_rule_data,
        )

    def get_passport_rule(
        self,
        db: Session,
        passport_rule_id: int,
    ) -> PassportRule:
        """Retrieve a passport rule by ID."""

        passport_rule = self.crud.get_by_id(
            db=db,
            obj_id=passport_rule_id,
        )

        if passport_rule is None:
            raise PassportRuleNotFoundError(
                passport_rule_id,
            )

        return passport_rule

    def get_all_passport_rules(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[PassportRule]:
        """Retrieve all passport rules."""


        return self.crud.get_all(db, skip, limit)

    def update_passport_rule(
        self,
        db: Session,
        passport_rule_id: int,
        passport_rule_data: PassportRuleUpdate,
    ) -> PassportRule:
        """Update an existing passport rule."""

        passport_rule = self.get_passport_rule(
            db=db,
            passport_rule_id=passport_rule_id,
        )

        update_data = passport_rule_data.model_dump(
            exclude_unset=True,
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != passport_rule.rule_id
        ):
            existing = (
                self.passport_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise PassportRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=passport_rule,
            data=passport_rule_data,
        )

    def delete_passport_rule(
        self,
        db: Session,
        passport_rule_id: int,
    ) -> None:
        """Delete a passport rule."""

        passport_rule = self.get_passport_rule(
            db=db,
            passport_rule_id=passport_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=passport_rule,
        )