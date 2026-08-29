from sqlalchemy.orm import Session

from src.rule_engine.models import (
    ComplianceContext,
    LoadedRules,
    TransitRuleEntry,
)
from src.services.rule_engine.rule_query_service import (
    RuleQueryService,
)
from src.models.compliance.passport_rule import PassportRule
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
    Loads all applicable compliance rules for a traveller,
    including per-transit-point transit rules.
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
            travel_date=context.travel_date,
        )

        # Load transit rules for each transit point
        transit_rules: list[TransitRuleEntry] = []

        for tp in context.transit_points:
            if tp.country_id and tp.airport_id:
                transit_rule = (
                    self.rule_query_service.get_transit_rule(
                        nationality_country_id=(
                            context.nationality_country_id
                        ),
                        transit_country_id=tp.country_id,
                        transit_airport_id=tp.airport_id,
                        travel_date=context.travel_date,
                    )
                )
            else:
                transit_rule = None

            transit_rules.append(
                TransitRuleEntry(
                    transit_point=tp,
                    transit_rule=transit_rule,
                )
            )

        return LoadedRules(
            visa_rule=visa_rule,
            passport_rule=self._load_passport_rule(context),
            health_rule=self._load_health_rule(context),
            immigration_rule=self._load_immigration_rule(
                context,
            ),
            customs_rule=self._load_customs_rule(context),
            entry_restriction=self._load_entry_restriction(
                context,
            ),
            transit_rules=transit_rules,
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
            travel_date=context.travel_date,
        )

    def _load_health_rule(
        self,
        context: ComplianceContext,
    ) -> HealthRule | None:

        return self.rule_query_service.get_health_rule(
            nationality_country_id=context.nationality_country_id,
            destination_country_id=context.destination_country_id,
            origin_country_id=context.origin_country_id,
            travel_date=context.travel_date,
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
            travel_date=context.travel_date,
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
            travel_date=context.travel_date,
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
            origin_country_id=context.origin_country_id,
            travel_date=context.travel_date,
        )