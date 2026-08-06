from sqlalchemy.orm import Session

from src.rule_engine.models import (
    ComplianceContext,
    LoadedRules,
)
from src.services.rule_engine.rule_query_service import (
    RuleQueryService,
)
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.transit_rule import TransitRule
from src.models.compliance.health_rule import HealthRule
from src.models.compliance.immigration_rule import (
    ImmigrationRule,
)
from src.models.compliance.customs_rule import CustomsRule
from src.models.compliance.entry_restriction import (
    EntryRestriction,
)
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
            transit_rule=self._load_transit_rule(context),
            health_rule=self._load_health_rule(context),
            immigration_rule=self._load_immigration_rule(context),
            customs_rule=self._load_customs_rule(context),
            entry_restriction=self._load_entry_restriction(context),
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

    def _load_transit_rule(
        self,
        context: ComplianceContext,
    ) -> TransitRule | None:
        """
        Load the applicable transit rule.
        """

        return self.rule_query_service.get_transit_rule(
            nationality_country_id=context.nationality_country_id,
            transit_country_id=context.destination_country_id,
            transit_airport_id=4,
        )

    def _load_health_rule(
        self,
        context: ComplianceContext,
    ) -> HealthRule | None:

        return self.rule_query_service.get_health_rule(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
        )

    def _load_immigration_rule(
        self,
        context: ComplianceContext,
    ) -> ImmigrationRule | None:
        """
        Load the applicable immigration rule.
        """

        return self.rule_query_service.get_immigration_rule(
            destination_country_id=context.destination_country_id,
        )

    def _load_customs_rule(
        self,
        context: ComplianceContext,
    ) -> CustomsRule | None:
        """
        Load the applicable customs rule.
        """

        return self.rule_query_service.get_customs_rule(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
        )

    def _load_entry_restriction(
        self,
        context: ComplianceContext,
    ) -> EntryRestriction | None:
        """
        Load the applicable entry restriction.
        """

        return self.rule_query_service.get_entry_restriction(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
        )