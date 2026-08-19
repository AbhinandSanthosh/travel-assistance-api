from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from src.schemas.common import StrictInputSchema


class AutoCheckRequest(StrictInputSchema):
    """What a client submits to /autocheck: traveller details."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "nationality": "India",
                "origin": "Saudi Arabia",
                "destination": "Poland",
                "purpose": "TOUR",
                "passport_type": "PP",
            }
        }
    )

    nationality: str = Field(
        ...,
        description="Traveller's nationality (country name), e.g. 'India'.",
    )
    origin: str | None = Field(
        None,
        description=(
            "Country the traveller is departing/embarking from for this "
            "journey, e.g. 'Saudi Arabia' for an Indian national flying "
            "to Poland via Riyadh. Optional — omit when travelling "
            "directly from the nationality country. Some health and "
            "entry-restriction requirements (e.g. Yellow Fever "
            "certificates for travellers arriving from a risk country) "
            "depend on this and not just nationality."
        ),
    )
    destination: str = Field(
        ...,
        description="Destination country name, e.g. 'Poland'.",
    )
    purpose: str = Field(
        ...,
        description=(
            "Purpose CODE from GET /purposes, e.g. 'TOUR' — not the "
            "display name ('Tourism'). Either is accepted, but the code "
            "is what the field is meant to hold."
        ),
    )
    passport_type: str = Field(
        ...,
        description=(
            "Passport type CODE from GET /passport-types, e.g. 'PP' for "
            "ordinary passport — not the display name."
        ),
    )


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