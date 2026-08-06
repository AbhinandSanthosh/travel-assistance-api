from sqlalchemy.orm import Session

from src.rule_engine.models import (
    ComplianceContext,
    LoadedRules,
)
from src.services.rule_engine.rule_query_service import (
    RuleQueryService,
)
from src.models.compliance.passport_rule import PassportRule

class RuleLoader:
    """
    Loads all applicable compliance rules for a traveller.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.rule_query_service = RuleQueryService(db)

    def load(
        self,
        context: ComplianceContext,
    ) -> LoadedRules:
        """
        Load all applicable rules based on the traveller context.
        """

        visa_rule = self.rule_query_service.get_visa_rule(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
            passport_type_id=context.passport_type_id,
            purpose_id=context.purpose_id,
        )

        return LoadedRules(
            visa_rule=visa_rule,
            passport_rule=self._load_passport_rule(context),
            transit_rule=None,
            health_rule=None,
            immigration_rule=None,
            customs_rule=None,
            entry_restriction=None,
        )

    def _load_passport_rule(
        self,
        context: ComplianceContext,
    ) -> PassportRule | None:
        """
        Load the applicable passport rule.
        """

        return self.rule_query_service.get_passport_rule(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
            passport_type_id=context.passport_type_id,
        )