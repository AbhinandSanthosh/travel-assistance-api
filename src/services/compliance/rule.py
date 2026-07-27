from sqlalchemy.orm import Session

from src.exceptions.rule import (
    RuleAlreadyExistsError,
    RuleNotFoundError,
)
from src.models.compliance.rule import Rule
from src.repositories.compliance.rule import RuleRepository
from src.schemas.compliance.rule import (
    RuleCreate,
    RuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class RuleService:
    """Service layer for Rule business logic."""

    def __init__(
        self,
        rule_repository: RuleRepository,
    ) -> None:
        self.rule_repository = rule_repository
        self.crud = BaseCrudService(rule_repository)

    def create_rule(
        self,
        db: Session,
        rule_data: RuleCreate,
    ) -> Rule:
        """Create a new rule."""

        if (
            self.rule_repository.get_by_rule_code(
                db,
                rule_data.rule_code,
            )
            is not None
        ):
            raise RuleAlreadyExistsError(
                field="rule_code",
                value=rule_data.rule_code,
            )

        return self.crud.create(
            db=db,
            model=Rule,
            data=rule_data,
        )
    
    def get_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> Rule:
        """Retrieve a rule by ID."""

        rule = self.crud.get_by_id(
            db=db,
            obj_id=rule_id,
        )

        if rule is None:
            raise RuleNotFoundError(rule_id)

        return rule
        
    def get_all_rules(
        self,
        db: Session,
    ) -> list[Rule]:
        """Retrieve all rules."""

        return self.crud.get_all(db)

    def update_rule(
        self,
        db: Session,
        rule_id: int,
        rule_data: RuleUpdate,
    ) -> Rule:
        """Update an existing rule."""

        rule = self.get_rule(
            db=db,
            rule_id=rule_id,
        )

        update_data = rule_data.model_dump(
            exclude_unset=True,
        )

        if (
            "rule_code" in update_data
            and update_data["rule_code"] != rule.rule_code
        ):
            existing = self.rule_repository.get_by_rule_code(
                db,
                update_data["rule_code"],
            )

            if existing is not None:
                raise RuleAlreadyExistsError(
                    field="rule_code",
                    value=update_data["rule_code"],
                )

        return self.crud.update(
            db=db,
            obj=rule,
            data=rule_data,
        )

    def delete_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> None:
        """Delete a rule."""

        rule = self.get_rule(
            db=db,
            rule_id=rule_id,
        )

        self.crud.delete(
            db=db,
            obj=rule,
        )