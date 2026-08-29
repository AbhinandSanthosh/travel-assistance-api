from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.common import StrictInputSchema


# ------------------------------------------------------------------ #
# Request schemas
# ------------------------------------------------------------------ #


class PassportInput(StrictInputSchema):
    """Passport details."""

    type: str = Field(
        ...,
        description=(
            "Passport type code: ORDINARY, DIPLOMATIC, "
            "SERVICE, EMERGENCY, etc."
        ),
    )
    country: str = Field(
        ...,
        description="Issuing country (ISO 3166-1 alpha-2).",
    )
    valid_until: date = Field(
        ...,
        description="Passport expiry date.",
    )
    valid_from: date | None = Field(
        None,
        description="Passport issue date.",
    )
    blank_pages: int | None = Field(
        None,
        description="Number of remaining blank pages.",
    )


class ExistingVisaInput(StrictInputSchema):
    """A visa the passenger already holds."""

    type: str = Field(
        ...,
        description="Visa type (e.g. SCHENGEN, TOURIST).",
    )
    issuing_country: str = Field(
        ...,
        description="Country that issued the visa (ISO alpha-2).",
    )
    valid_from: date | None = None
    valid_until: date | None = None
    entries: str | None = Field(
        None,
        description="SINGLE, MULTIPLE, or UNLIMITED.",
    )


class PassengerInput(StrictInputSchema):
    """Deep passenger profile."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "nationality": "IN",
                "passport": {
                    "type": "ORDINARY",
                    "country": "IN",
                    "valid_until": "2027-04-15",
                },
            }
        },
    )

    nationality: str = Field(
        ...,
        description=(
            "Passenger nationality (ISO 3166-1 alpha-2)."
        ),
    )
    country_of_residence: str | None = Field(
        None,
        description="Country of residence (ISO alpha-2).",
    )
    passport: PassportInput
    existing_visas: list[ExistingVisaInput] = Field(
        default_factory=list,
    )
    passenger_type: str | None = Field(
        None,
        description="ADULT, CHILD, INFANT, or CREW.",
    )
    special_status: str | None = Field(
        None,
        description=(
            "DIPLOMAT, REFUGEE, STATELESS, "
            "SEAMAN, MILITARY."
        ),
    )


class JourneySegmentInput(StrictInputSchema):
    """A single flight leg."""

    departure_airport: str = Field(
        ...,
        description="IATA airport code (e.g. COK).",
    )
    arrival_airport: str = Field(
        ...,
        description="IATA airport code (e.g. DOH).",
    )
    airline: str | None = None
    flight_number: str | None = None
    departure_datetime: datetime | None = None


class TransitPointInput(StrictInputSchema):
    """A transit stop."""

    airport: str = Field(
        ...,
        description="IATA code of the transit airport.",
    )
    duration_minutes: int | None = None
    requires_immigration: bool = False
    separate_ticket: bool = False


class JourneyInput(StrictInputSchema):
    """Complete journey / itinerary."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "origin": "COK",
                "destination": "FRA",
                "travel_date": "2026-09-15",
                "purpose": "TOURISM",
            }
        },
    )

    origin: str = Field(
        ...,
        description="Origin airport IATA code.",
    )
    destination: str = Field(
        ...,
        description="Destination airport IATA code.",
    )
    travel_date: date
    return_date: date | None = None
    purpose: str = Field(
        ...,
        description=(
            "Travel purpose code "
            "(e.g. TOUR, BUSINESS, WORK)."
        ),
    )
    segments: list[JourneySegmentInput] = Field(
        default_factory=list,
    )
    transit_points: list[TransitPointInput] = Field(
        default_factory=list,
    )


class TravelRequirementsCheckRequest(StrictInputSchema):
    """Primary TISCO check request: passenger + journey."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "passenger": {
                    "nationality": "IN",
                    "passport": {
                        "type": "ORDINARY",
                        "country": "IN",
                        "valid_until": "2027-04-15",
                    },
                },
                "journey": {
                    "origin": "COK",
                    "destination": "FRA",
                    "travel_date": "2026-09-15",
                    "purpose": "TOURISM",
                },
            }
        },
    )

    passenger: PassengerInput
    journey: JourneyInput


# ------------------------------------------------------------------ #
# Response schemas
# ------------------------------------------------------------------ #


class SubRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str
    name: str
    status: str
    details: str | None = None


class RequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str
    status: str
    title: str
    details: str
    sub_requirements: list[SubRequirementResponse] = []
    applicable_rule: str | None = None
    applicable_rule_code: str | None = None
    source: str | None = None
    effective_from: date | None = None
    effective_until: date | None = None


class JourneySummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    origin: str
    destination: str
    transit_countries: list[str] = []


class RuleExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rule_id: str
    rule_code: str
    domain: str
    matched: bool
    reason: str | None = None


class TravelRequirementsCheckResponse(BaseModel):
    """Full TISCO check response."""

    check_id: str
    decision: str
    summary: str
    requirements: list[RequirementResponse]
    warnings: list[RequirementResponse]
    journey: JourneySummaryResponse
    rule_execution_log: list[RuleExecutionResponse] = []
    evaluated_at: datetime
    rule_version: str
