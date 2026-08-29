from sqlalchemy.orm import Session

from src.exceptions.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleAlreadyExistsError,
    TravelAuthorizationRuleNotFoundError,
)
from src.models.compliance.travel_authorization_rule import (
    TravelAuthorizationRule,
)
from src.repositories.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleRepository,
)
from src.schemas.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleCreate,
    TravelAuthorizationRuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class TravelAuthorizationRuleService:
    """Service layer for TravelAuthorizationRule business logic."""

    def __init__(
        self,
        travel_authorization_rule_repository: TravelAuthorizationRuleRepository,
    ) -> None:
        self.travel_authorization_rule_repository = (
            travel_authorization_rule_repository
        )
        self.crud = BaseCrudService(
            travel_authorization_rule_repository,
        )

    def create_travel_authorization_rule(
        self,
        db: Session,
        travel_authorization_rule_data: (
            TravelAuthorizationRuleCreate
        ),
    ) -> TravelAuthorizationRule:
        """Create a new travel authorization rule."""

        if (
            self.travel_authorization_rule_repository.get_by_rule_id(
                db,
                travel_authorization_rule_data.rule_id,
            )
            is not None
        ):
            raise TravelAuthorizationRuleAlreadyExistsError(
                field="rule_id",
                value=travel_authorization_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=TravelAuthorizationRule,
            data=travel_authorization_rule_data,
        )

    def get_travel_authorization_rule(
        self,
        db: Session,
        travel_authorization_rule_id: int,
    ) -> TravelAuthorizationRule:
        """Retrieve a travel authorization rule by ID."""

        travel_authorization_rule = self.crud.get_by_id(
            db=db,
            obj_id=travel_authorization_rule_id,
        )

        if travel_authorization_rule is None:
            raise TravelAuthorizationRuleNotFoundError(
                travel_authorization_rule_id,
            )

        return travel_authorization_rule

    def get_all_travel_authorization_rules(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TravelAuthorizationRule]:
        """Retrieve all travel authorization rules."""


        return self.crud.get_all(db, skip, limit)

    def update_travel_authorization_rule(
        self,
        db: Session,
        travel_authorization_rule_id: int,
        travel_authorization_rule_data: (
            TravelAuthorizationRuleUpdate
        ),
    ) -> TravelAuthorizationRule:
        """Update an existing travel authorization rule."""

        travel_authorization_rule = (
            self.get_travel_authorization_rule(
                db=db,
                travel_authorization_rule_id=(
                    travel_authorization_rule_id
                ),
            )
        )

        update_data = (
            travel_authorization_rule_data.model_dump(
                exclude_unset=True,
            )
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"]
            != travel_authorization_rule.rule_id
        ):
            existing = (
                self.travel_authorization_rule_repository.get_by_rule_id(
                    db,
                    update_data["rule_id"],
                )
            )

            if existing is not None:
                raise (
                    TravelAuthorizationRuleAlreadyExistsError(
                        field="rule_id",
                        value=update_data["rule_id"],
                    )
                )

        return self.crud.update(
            db=db,
            obj=travel_authorization_rule,
            data=travel_authorization_rule_data,
        )

    def delete_travel_authorization_rule(
        self,
        db: Session,
        travel_authorization_rule_id: int,
    ) -> None:
        """Delete a travel authorization rule."""

        travel_authorization_rule = (
            self.get_travel_authorization_rule(
                db=db,
                travel_authorization_rule_id=(
                    travel_authorization_rule_id
                ),
            )
        )

        self.crud.delete(
            db=db,
            obj=travel_authorization_rule,
        )