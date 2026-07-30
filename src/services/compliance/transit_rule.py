from sqlalchemy.orm import Session

from src.exceptions.compliance.transit_rule import (
    TransitRuleAlreadyExistsError,
    TransitRuleNotFoundError,
)
from src.models.compliance.transit_rule import TransitRule
from src.repositories.compliance.transit_rule import (
    TransitRuleRepository,
)
from src.schemas.compliance.transit_rule import (
    TransitRuleCreate,
    TransitRuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class TransitRuleService:
    """Service layer for TransitRule business logic."""

    def __init__(
        self,
        transit_rule_repository: TransitRuleRepository,
    ) -> None:
        self.transit_rule_repository = (
            transit_rule_repository
        )
        self.crud = BaseCrudService(
            transit_rule_repository,
        )

    def create_transit_rule(
        self,
        db: Session,
        transit_rule_data: TransitRuleCreate,
    ) -> TransitRule:
        """Create a new transit rule."""

        if (
            self.transit_rule_repository.get_by_rule_id(
                db,
                transit_rule_data.rule_id,
            )
            is not None
        ):
            raise TransitRuleAlreadyExistsError(
                field="rule_id",
                value=transit_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=TransitRule,
            data=transit_rule_data,
        )

    def get_transit_rule(
        self,
        db: Session,
        transit_rule_id: int,
    ) -> TransitRule:
        """Retrieve a transit rule by ID."""

        transit_rule = self.crud.get_by_id(
            db=db,
            obj_id=transit_rule_id,
        )

        if transit_rule is None:
            raise TransitRuleNotFoundError(
                transit_rule_id,
            )

        return transit_rule

    def get_all_transit_rules(
        self,
        db: Session,
    ) -> list[TransitRule]:
        """Retrieve all transit rules."""

        return self.crud.get_all(db)

    def update_transit_rule(
        self,
        db: Session,
        transit_rule_id: int,
        transit_rule_data: TransitRuleUpdate,
    ) -> TransitRule:
        """Update an existing transit rule."""

        transit_rule = self.get_transit_rule(
            db=db,
            transit_rule_id=transit_rule_id,
        )

        update_data = transit_rule_data.model_dump(
            exclude_unset=True,
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != transit_rule.rule_id
        ):
            existing = (
                self.transit_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise TransitRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=transit_rule,
            data=transit_rule_data,
        )

    def delete_transit_rule(
        self,
        db: Session,
        transit_rule_id: int,
    ) -> None:
        """Delete a transit rule."""

        transit_rule = self.get_transit_rule(
            db=db,
            transit_rule_id=transit_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=transit_rule,
        )