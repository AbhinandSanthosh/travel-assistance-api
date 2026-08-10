from datetime import date

from src.rule_engine.models import (
    ComplianceContext,
    NormalizedJourney,
)


class ContextBuilder:
    """
    Builds the shared compliance context
    used by all evaluators.
    """

    def build(
        self,
        journey: NormalizedJourney,
        travel_date: date,
    ) -> ComplianceContext:

        return ComplianceContext(
            nationality_country_id=journey.nationality_country_id,
            destination_country_id=journey.destination_country_id,
            purpose_id=journey.purpose_id,
            passport_type_id=journey.passport_type_id,
            travel_date=travel_date,
            origin_country_id=journey.origin_country_id,
        )