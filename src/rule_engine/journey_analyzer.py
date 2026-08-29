from sqlalchemy.orm import Session

from src.domain.journey import TransitPoint
from src.rule_engine.models import (
    JourneyRequest,
    NormalizedJourney,
)
from src.rule_engine.reference_resolver import (
    ReferenceResolver,
)


class JourneyAnalyzer:
    """
    Converts a rich journey request into a normalized journey
    with resolved country IDs, airport IDs, and transit points.
    """

    def __init__(self, db: Session):
        self.resolver = ReferenceResolver(db)

    def analyze(
        self,
        request: JourneyRequest,
    ) -> NormalizedJourney:

        passenger = request.passenger
        journey = request.journey

        # Resolve origin and destination airports
        origin_airport = self.resolver.get_airport(
            journey.origin,
        )
        dest_airport = self.resolver.get_airport(
            journey.destination,
        )

        # Resolve nationality (ISO alpha-2 code)
        nationality = self.resolver.get_country_by_iso2(
            passenger.nationality,
        )

        # Resolve purpose and passport type
        purpose = self.resolver.get_purpose(journey.purpose)
        passport_type = self.resolver.get_passport_type(
            passenger.passport.type,
        )

        # Derive transit points from segments if not provided
        transit_points = list(journey.transit_points)

        if not transit_points and len(journey.segments) > 1:
            transit_points = self._derive_transit_points(
                journey.segments,
            )

        # Resolve each transit point's airport → country
        resolved_transit: list[TransitPoint] = []

        for tp in transit_points:
            tp_airport = self.resolver.get_airport(tp.airport)

            resolved_transit.append(
                TransitPoint(
                    airport=tp.airport,
                    country=tp_airport.country.iso2,
                    country_id=tp_airport.country_id,
                    airport_id=tp_airport.id,
                    duration_minutes=tp.duration_minutes,
                    requires_immigration=tp.requires_immigration,
                    separate_ticket=tp.separate_ticket,
                )
            )

        return NormalizedJourney(
            nationality_country_id=nationality.id,
            destination_country_id=dest_airport.country_id,
            origin_country_id=origin_airport.country_id,
            purpose_id=purpose.id,
            passport_type_id=passport_type.id,
            travel_date=journey.travel_date,
            transit_points=resolved_transit,
            destination_airport_id=dest_airport.id,
            origin_airport_id=origin_airport.id,
        )

    @staticmethod
    def _derive_transit_points(segments) -> list[TransitPoint]:
        """Derive transit points from flight segments.

        For segments A→B, B→C, C→D: transit points are B and C.
        """

        transit_points = []

        for i in range(len(segments) - 1):
            arrival = segments[i].arrival_airport
            transit_points.append(
                TransitPoint(airport=arrival),
            )

        return transit_points