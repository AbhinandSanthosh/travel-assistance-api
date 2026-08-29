from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from src.schemas.common import StrictInputSchema


class PassportInfoRequest(StrictInputSchema):
    """Passport the passenger will travel on."""

    issuing_country: str = Field(
        ..., description="ISO 3166-1 alpha-2 code, e.g. 'IN'.",
    )
    type: str = Field(
        ...,
        description=(
            "Passport type CODE from GET /passport-types, e.g. 'PP' "
            "for ordinary."
        ),
    )
    valid_until: date
    valid_from: date | None = None
    blank_pages: int | None = None


class ExistingVisaRequest(StrictInputSchema):
    """A visa the passenger already holds -- may satisfy a
    destination or transit requirement without needing a new one."""

    type: str = Field(..., description="e.g. SCHENGEN, TOURIST, WORK.")
    issuing_country: str = Field(..., description="ISO alpha-2.")
    valid_from: date | None = None
    valid_until: date | None = None
    entries: str | None = Field(
        default=None, description="SINGLE, MULTIPLE, or UNLIMITED.",
    )


class PassengerRequest(StrictInputSchema):
    """Complete passenger profile for the journey being checked."""

    nationality: str = Field(
        ..., description="ISO alpha-2 code of citizenship, e.g. 'IN'.",
    )
    passport: PassportInfoRequest
    country_of_residence: str | None = Field(
        default=None,
        description="ISO alpha-2, if different from nationality.",
    )
    existing_visas: list[ExistingVisaRequest] = Field(default_factory=list)
    passenger_type: str | None = Field(
        default=None, description="ADULT, CHILD, INFANT, or CREW.",
    )
    special_status: str | None = Field(
        default=None,
        description="DIPLOMAT, REFUGEE, STATELESS, SEAMAN, MILITARY, or omit.",
    )


class JourneySegmentRequest(StrictInputSchema):
    """A single flight leg. Only needed for multi-leg itineraries --
    for a direct route, just set journey.origin/destination."""

    departure_airport: str = Field(..., description="IATA code, e.g. 'COK'.")
    arrival_airport: str = Field(..., description="IATA code, e.g. 'DOH'.")
    airline: str | None = None
    flight_number: str | None = None
    departure_datetime: datetime | None = None


class TransitPointRequest(StrictInputSchema):
    """An intermediate stop, when known explicitly rather than
    derived from `segments`. The transit country/airport are resolved
    server-side from the IATA code -- don't send them."""

    airport: str = Field(..., description="IATA code of the connecting airport.")
    duration_minutes: int | None = None
    requires_immigration: bool = False
    separate_ticket: bool = False


class JourneyRequestSchema(StrictInputSchema):
    """Itinerary for the check. Provide EITHER just origin+destination
    (direct route assumed), OR explicit transit_points, OR a full
    segments list -- transit points are derived automatically from
    segments if not given explicitly."""

    origin: str = Field(..., description="IATA airport code, e.g. 'COK'.")
    destination: str = Field(..., description="IATA airport code, e.g. 'FRA'.")
    travel_date: date
    purpose: str = Field(
        ..., description="Purpose CODE from GET /purposes, e.g. 'TOUR'.",
    )
    return_date: date | None = None
    segments: list[JourneySegmentRequest] = Field(default_factory=list)
    transit_points: list[TransitPointRequest] = Field(default_factory=list)


class AutoCheckRequest(StrictInputSchema):
    """What a client submits to /autocheck: full passenger + journey."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "passenger": {
                    "nationality": "IN",
                    "passport": {
                        "issuing_country": "IN",
                        "type": "PP",
                        "valid_until": "2027-04-15",
                    },
                },
                "journey": {
                    "origin": "COK",
                    "destination": "FRA",
                    "travel_date": "2026-09-15",
                    "purpose": "TOUR",
                },
            }
        },
    )

    passenger: PassengerRequest
    journey: JourneyRequestSchema


class VisaRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    visa_required: bool
    visa_type: str | None
    visa_on_arrival: bool
    evisa_available: bool
    max_stay_days: int | None
    multiple_entry: bool
    remarks: str | None


class PassportRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    minimum_validity_months: int | None
    blank_pages_required: int | None
    machine_readable_required: bool | None
    damaged_passport_allowed: bool | None
    temporary_passport_allowed: bool | None
    passport_issue_date_required: bool | None
    remarks: str | None


class TransitRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transit_visa_required: bool
    airside_transit_allowed: bool
    baggage_collection_required: bool
    overnight_transit_allowed: bool
    max_transit_hours: int | None
    remarks: str | None


class VaccineRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vaccine_name: str
    certificate_required: bool


class HealthRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    health_form_required: bool
    quarantine_required: bool
    quarantine_days: int | None
    medical_certificate_required: bool
    vaccines: list[VaccineRequirementResponse]
    remarks: str | None


class ImmigrationRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    onward_ticket_required: bool
    accommodation_proof_required: bool
    proof_of_funds_required: bool
    biometric_required: bool
    interview_required: bool
    arrival_card_required: bool
    digital_arrival_card: bool
    arrival_registration_required: bool
    remarks: str | None


class CustomsRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alcohol_limit: str | None
    tobacco_limit: str | None
    currency_limit_amount: Decimal | None
    currency: str | None
    currency_declaration_required: bool
    medication_rules: str | None
    prohibited_items: str | None
    restricted_items: str | None
    pet_import_rules: str | None
    remarks: str | None


class EntryRestrictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    restriction_type: str
    reason: str | None
    effective_date: date
    expiry_date: date | None
    source: str | None
    remarks: str | None


class ComplianceDecisionResponse(BaseModel):
    """Mirrors src.rule_engine.models.ComplianceDecision."""

    model_config = ConfigDict(from_attributes=True)

    status: str
    summary: str
    requirements: list[str]
    warnings: list[str]
    blockers: list[str]


class AutoCheckResponse(BaseModel):
    """Full result of a /autocheck call: the final decision plus the
    detailed, per-category travel requirements for this nationality ->
    destination pair, exactly what should be shown to a traveller."""

    compliance_check_id: int
    request_id: str

    nationality: str
    origin: str | None = None
    destination: str
    purpose: str
    passport_type: str

    decision: ComplianceDecisionResponse

    visa: VisaRequirementResponse | None = None
    passport: PassportRequirementResponse | None = None
    transit: TransitRequirementResponse | None = None
    health: HealthRequirementResponse | None = None
    immigration: ImmigrationRequirementResponse | None = None
    customs: CustomsRequirementResponse | None = None
    entry_restriction: EntryRestrictionResponse | None = None


class ValidateKeyResponse(BaseModel):
    """Result of POST /autocheck/validate-key: confirms the key is
    valid, active, and whitelisted for the caller's IP, without running
    the rule engine."""

    valid: bool = True
    client_name: str
    company_name: str