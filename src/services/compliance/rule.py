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


class RuleService:
    """Service layer for Rule business logic."""

    def __init__(
        self,
        rule_repository: RuleRepository,
    ):
        self.rule_repository = rule_repository

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

        rule = Rule(**rule_data.model_dump())

        return self.rule_repository.create(
            db=db,
            obj=rule,
        )

    def get_rule(
        self,
        db: Session,
        rule_id: int,
    ) -> Rule:
        """Retrieve a rule by ID."""

        rule = self.rule_repository.get_by_id(
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

        return self.rule_repository.get_all(db)

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

        for field, value in update_data.items():
            setattr(
                rule,
                field,
                value,
            )

        return self.rule_repository.save(
            db=db,
            obj=rule,
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

        self.rule_repository.delete(
            db=db,
            obj=rule,
        )