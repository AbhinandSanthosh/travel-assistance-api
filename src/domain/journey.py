"""
Full itinerary model for the TISCO Decision Engine.

Models a complete journey with flight segments, transit points, and
travel metadata. The journey analyzer decomposes this into individual
legs and resolves each airport code to its country, enabling the rule
engine to evaluate transit requirements independently for every
intermediate stop.

Example:
    COK → DOH → FRA becomes:
        origin_country  = India
        transit_country = Qatar   (transit point at DOH)
        dest_country    = Germany

    The engine evaluates destination rules for Germany AND transit
    rules for Qatar independently.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class JourneySegment:
    """A single flight leg within the itinerary."""

    departure_airport: str            # IATA code (e.g. COK)
    arrival_airport: str              # IATA code (e.g. DOH)
    airline: str | None = None        # IATA airline code
    flight_number: str | None = None
    departure_datetime: datetime | None = None


@dataclass
class TransitPoint:
    """An intermediate stop where the passenger connects.

    Attributes:
        airport: IATA code of the connecting airport.
        country: ISO alpha-2 code, resolved from the airport reference.
        country_id: Database ID of the transit country (populated
            by the JourneyAnalyzer after reference resolution).
        airport_id: Database ID of the transit airport.
        duration_minutes: Layover duration when known.
        requires_immigration: True if the passenger must clear
            immigration at this point (e.g. separate tickets,
            terminal change requiring exit/re-entry, >24h layover).
        separate_ticket: True if the connecting flight is on a
            separate ticket (baggage will not transfer).
    """

    airport: str
    country: str = ""
    country_id: int | None = None
    airport_id: int | None = None
    duration_minutes: int | None = None
    requires_immigration: bool = False
    separate_ticket: bool = False


@dataclass
class Journey:
    """Complete journey submitted with a check request.

    Callers may provide either:
    1. Just origin + destination (direct route assumed), or
    2. origin + destination + explicit transit_points, or
    3. Full segments list (transit points derived automatically).

    The JourneyAnalyzer normalizes all three representations into
    a consistent internal form with resolved country IDs.
    """

    origin: str                       # IATA airport code
    destination: str                  # IATA airport code
    travel_date: date
    purpose: str
    return_date: date | None = None
    segments: list[JourneySegment] = field(default_factory=list)
    transit_points: list[TransitPoint] = field(default_factory=list)
