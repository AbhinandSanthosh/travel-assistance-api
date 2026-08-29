from sqlalchemy.orm import Session

from src.exceptions.compliance.immigration_rule import (
    ImmigrationRuleAlreadyExistsError,
    ImmigrationRuleNotFoundError,
)
from src.models.compliance.immigration_rule import (
    ImmigrationRule,
)
from src.repositories.compliance.immigration_rule import (
    ImmigrationRuleRepository,
)
from src.schemas.compliance.immigration_rule import (
    ImmigrationRuleCreate,
    ImmigrationRuleUpdate,
)
from src.services.base_crud_service import (
    BaseCrudService,
)


class ImmigrationRuleService:
    """Service layer for ImmigrationRule business logic."""

    def __init__(
        self,
        immigration_rule_repository: ImmigrationRuleRepository,
    ) -> None:
        self.immigration_rule_repository = (
            immigration_rule_repository
        )
        self.crud = BaseCrudService(
            immigration_rule_repository,
        )

    def create_immigration_rule(
        self,
        db: Session,
        immigration_rule_data: ImmigrationRuleCreate,
    ) -> ImmigrationRule:
        """Create a new immigration rule."""

        if (
            self.immigration_rule_repository.get_by_rule_id(
                db,
                immigration_rule_data.rule_id,
            )
            is not None
        ):
            raise ImmigrationRuleAlreadyExistsError(
                field="rule_id",
                value=immigration_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=ImmigrationRule,
            data=immigration_rule_data,
        )

    def get_immigration_rule(
        self,
        db: Session,
        immigration_rule_id: int,
    ) -> ImmigrationRule:
        """Retrieve an immigration rule by ID."""

        immigration_rule = self.crud.get_by_id(
            db=db,
            obj_id=immigration_rule_id,
        )

        if immigration_rule is None:
            raise ImmigrationRuleNotFoundError(
                immigration_rule_id,
            )

        return immigration_rule

    def get_all_immigration_rules(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ImmigrationRule]:
        """Retrieve all immigration rules."""


        return self.crud.get_all(db, skip, limit)

    def update_immigration_rule(
        self,
        db: Session,
        immigration_rule_id: int,
        immigration_rule_data: ImmigrationRuleUpdate,
    ) -> ImmigrationRule:
        """Update an existing immigration rule."""

        immigration_rule = self.get_immigration_rule(
            db=db,
            immigration_rule_id=immigration_rule_id,
        )

        update_data = (
            immigration_rule_data.model_dump(
                exclude_unset=True,
            )
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != immigration_rule.rule_id
        ):
            existing = (
                self.immigration_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise ImmigrationRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=immigration_rule,
            data=immigration_rule_data,
        )

    def delete_immigration_rule(
        self,
        db: Session,
        immigration_rule_id: int,
    ) -> None:
        """Delete an immigration rule."""

        immigration_rule = self.get_immigration_rule(
            db=db,
            immigration_rule_id=immigration_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=immigration_rule,
        )