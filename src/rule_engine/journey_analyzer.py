from sqlalchemy.orm import Session

from src.rule_engine.models import (
    JourneyRequest,
    NormalizedJourney,
)
from src.rule_engine.reference_resolver import (
    ReferenceResolver,
)


class JourneyAnalyzer:
    """
    Converts a user journey request into a normalized
    journey using reference/master data.
    """

    def __init__(self, db: Session):
        self.resolver = ReferenceResolver(db)

    def analyze(
        self,
        request: JourneyRequest,
    ) -> NormalizedJourney:

        nationality = self.resolver.get_country(
            request.nationality,
        )

        destination = self.resolver.get_country(
            request.destination,
        )

        purpose = self.resolver.get_purpose(
            request.purpose,
        )

        passport = self.resolver.get_passport_type(
            request.passport_type,
        )

        # origin (point of departure/embarkation) is optional: most
        # bookings originate from the traveller's nationality country,
        # so callers aren't required to send it. When present, it must
        # still resolve to a known country like any other reference field.
        origin_country_id = None

        if request.origin:
            origin = self.resolver.get_country(
                request.origin,
            )
            origin_country_id = origin.id

        return NormalizedJourney(
            nationality_country_id=nationality.id,
            destination_country_id=destination.id,
            purpose_id=purpose.id,
            passport_type_id=passport.id,
            origin_country_id=origin_country_id,
        )