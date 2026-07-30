from sqlalchemy.orm import Session

from src.exceptions.compliance.visa_rule import (
    VisaRuleAlreadyExistsError,
    VisaRuleNotFoundError,
)
from src.models.compliance.visa_rule import VisaRule
from src.repositories.compliance.visa_rule import VisaRuleRepository
from src.schemas.compliance.visa_rule import (
    VisaRuleCreate,
    VisaRuleUpdate,
)
from src.services.base_crud_service import BaseCrudService


class VisaRuleService:
    """Service layer for VisaRule business logic."""

    def __init__(
        self,
        visa_rule_repository: VisaRuleRepository,
    ) -> None:
        self.visa_rule_repository = visa_rule_repository
        self.crud = BaseCrudService(visa_rule_repository)

    def create_visa_rule(
        self,
        db: Session,
        visa_rule_data: VisaRuleCreate,
    ) -> VisaRule:
        """Create a new visa rule."""

        if (
            self.visa_rule_repository.get_by_rule_id(
                db,
                visa_rule_data.rule_id,
            )
            is not None
        ):
            raise VisaRuleAlreadyExistsError(
                field="rule_id",
                value=visa_rule_data.rule_id,
            )

        return self.crud.create(
            db=db,
            model=VisaRule,
            data=visa_rule_data,
        )

    def get_visa_rule(
        self,
        db: Session,
        visa_rule_id: int,
    ) -> VisaRule:
        """Retrieve a visa rule by ID."""

        visa_rule = self.crud.get_by_id(
            db=db,
            obj_id=visa_rule_id,
        )

        if visa_rule is None:
            raise VisaRuleNotFoundError(visa_rule_id)

        return visa_rule

    def get_all_visa_rules(
        self,
        db: Session,
    ) -> list[VisaRule]:
        """Retrieve all visa rules."""

        return self.crud.get_all(db)

    def update_visa_rule(
        self,
        db: Session,
        visa_rule_id: int,
        visa_rule_data: VisaRuleUpdate,
    ) -> VisaRule:
        """Update an existing visa rule."""

        visa_rule = self.get_visa_rule(
            db=db,
            visa_rule_id=visa_rule_id,
        )

        update_data = visa_rule_data.model_dump(
            exclude_unset=True,
        )

        if (
            "rule_id" in update_data
            and update_data["rule_id"] != visa_rule.rule_id
        ):
            existing = self.visa_rule_repository.get_by_rule_id(
                db,
                update_data["rule_id"],
            )

            if existing is not None:
                raise VisaRuleAlreadyExistsError(
                    field="rule_id",
                    value=update_data["rule_id"],
                )

        return self.crud.update(
            db=db,
            obj=visa_rule,
            data=visa_rule_data,
        )

    def delete_visa_rule(
        self,
        db: Session,
        visa_rule_id: int,
    ) -> None:
        """Delete a visa rule."""

        visa_rule = self.get_visa_rule(
            db=db,
            visa_rule_id=visa_rule_id,
        )

        self.crud.delete(
            db=db,
            obj=visa_rule,
        )