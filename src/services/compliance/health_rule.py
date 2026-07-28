from sqlalchemy.orm import Session

from src.exceptions.health_rule import (
    HealthRuleAlreadyExistsError,
    HealthRuleNotFoundError,
)
from src.models.compliance.health_rule import HealthRule
from src.repositories.compliance.health_rule import (
    HealthRuleRepository,
)
from src.schemas.compliance.health_rule import (
    HealthRuleCreate,
    HealthRuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class HealthRuleService:
    """Service layer for HealthRule business logic."""

    def __init__(
        self,
        health_rule_repository: HealthRuleRepository,
    ) -> None:
        self.health_rule_repository = (
            health_rule_repository
        )
        self.crud = BaseCrudService(
            health_rule_repository,
        )

    def create_health_rule(
        self,
        db: Session,
        health_rule_data: HealthRuleCreate,
    ) -> HealthRule:
        """Create a new health rule."""

        if (
            self.health_rule_repository.get_by_rule_id(
                db,
                health_rule_data.rule_id,
            )
            is not None
        ):
            raise HealthRuleAlreadyExistsError(
                field="rule_id",
                value=health_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=HealthRule,
            data=health_rule_data,
        )

    def get_health_rule(
        self,
        db: Session,
        health_rule_id: int,
    ) -> HealthRule:
        """Retrieve a health rule by ID."""

        health_rule = self.crud.get_by_id(
            db=db,
            obj_id=health_rule_id,
        )

        if health_rule is None:
            raise HealthRuleNotFoundError(
                health_rule_id,
            )

        return health_rule

    def get_all_health_rules(
        self,
        db: Session,
    ) -> list[HealthRule]:
        """Retrieve all health rules."""

        return self.crud.get_all(db)

    def update_health_rule(
        self,
        db: Session,
        health_rule_id: int,
        health_rule_data: HealthRuleUpdate,
    ) -> HealthRule:
        """Update an existing health rule."""

        health_rule = self.get_health_rule(
            db=db,
            health_rule_id=health_rule_id,
        )

        update_data = health_rule_data.model_dump(
            exclude_unset=True,
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != health_rule.rule_id
        ):
            existing = (
                self.health_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise HealthRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=health_rule,
            data=health_rule_data,
        )

    def delete_health_rule(
        self,
        db: Session,
        health_rule_id: int,
    ) -> None:
        """Delete a health rule."""

        health_rule = self.get_health_rule(
            db=db,
            health_rule_id=health_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=health_rule,
        )