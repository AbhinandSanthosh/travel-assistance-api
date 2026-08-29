from sqlalchemy.orm import Session

from src.exceptions.compliance.customs_rule import (
    CustomsRuleAlreadyExistsError,
    CustomsRuleNotFoundError,
)
from src.models.compliance.customs_rule import (
    CustomsRule,
)
from src.repositories.compliance.customs_rule import (
    CustomsRuleRepository,
)
from src.schemas.compliance.customs_rule import (
    CustomsRuleCreate,
    CustomsRuleUpdate,
)
from src.services.base_crud_service import (
    BaseCrudService,
)


class CustomsRuleService:
    """Service layer for CustomsRule business logic."""

    def __init__(
        self,
        customs_rule_repository: CustomsRuleRepository,
    ) -> None:
        self.customs_rule_repository = (
            customs_rule_repository
        )
        self.crud = BaseCrudService(
            customs_rule_repository,
        )

    def create_customs_rule(
        self,
        db: Session,
        customs_rule_data: CustomsRuleCreate,
    ) -> CustomsRule:
        """Create a new customs rule."""

        if (
            self.customs_rule_repository.get_by_rule_id(
                db,
                customs_rule_data.rule_id,
            )
            is not None
        ):
            raise CustomsRuleAlreadyExistsError(
                field="rule_id",
                value=customs_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=CustomsRule,
            data=customs_rule_data,
        )

    def get_customs_rule(
        self,
        db: Session,
        customs_rule_id: int,
    ) -> CustomsRule:
        """Retrieve a customs rule by ID."""

        customs_rule = self.crud.get_by_id(
            db=db,
            obj_id=customs_rule_id,
        )

        if customs_rule is None:
            raise CustomsRuleNotFoundError(
                customs_rule_id,
            )

        return customs_rule

    def get_all_customs_rules(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CustomsRule]:
        """Retrieve all customs rules."""


        return self.crud.get_all(db, skip, limit)

    def update_customs_rule(
        self,
        db: Session,
        customs_rule_id: int,
        customs_rule_data: CustomsRuleUpdate,
    ) -> CustomsRule:
        """Update an existing customs rule."""

        customs_rule = self.get_customs_rule(
            db=db,
            customs_rule_id=customs_rule_id,
        )

        update_data = (
            customs_rule_data.model_dump(
                exclude_unset=True,
            )
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != customs_rule.rule_id
        ):
            existing = (
                self.customs_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise CustomsRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=customs_rule,
            data=customs_rule_data,
        )

    def delete_customs_rule(
        self,
        db: Session,
        customs_rule_id: int,
    ) -> None:
        """Delete a customs rule."""

        customs_rule = self.get_customs_rule(
            db=db,
            customs_rule_id=customs_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=customs_rule,
        )