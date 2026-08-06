from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from src.models.compliance.customs_rule import CustomsRule
from src.models.compliance.entry_restriction import EntryRestriction
from src.models.compliance.health_rule import HealthRule
from src.models.compliance.immigration_rule import ImmigrationRule
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.transit_rule import TransitRule
from src.models.compliance.visa_rule import VisaRule


@dataclass
class JourneyRequest:
    """
    Raw journey request received from the API.
    """

    nationality: str
    destination: str
    purpose: str
    passport_type: str


@dataclass
class NormalizedJourney:
    """
    Journey after resolving all reference data IDs.
    """

    nationality_country_id: int
    destination_country_id: int
    purpose_id: int
    passport_type_id: int


@dataclass
class ComplianceContext:
    """
    Shared context passed to every Rule Engine component.
    """

    nationality_country_id: int
    destination_country_id: int
    purpose_id: int
    passport_type_id: int
    travel_date: date


@dataclass
class LoadedRules:
    """
    Collection of all rules applicable to the traveller.
    """

    visa_rule: VisaRule | None
    passport_rule: PassportRule | None
    transit_rule: TransitRule | None
    health_rule: HealthRule | None
    immigration_rule: ImmigrationRule | None
    customs_rule: CustomsRule | None
    entry_restriction: EntryRestriction | None

@dataclass
class VisaEvaluationResult:
    """
    Result produced by the Visa Evaluator.
    """

    visa_required: bool
    visa_type: str | None
    visa_on_arrival: bool
    evisa_available: bool
    max_stay_days: int | None
    multiple_entry: bool
    remarks: str | None
@dataclass
class PassportEvaluationResult:
    """
    Result produced by the Passport Evaluator.
    """

    minimum_validity_months: int | None

    blank_pages_required: int | None

    machine_readable_required: bool | None

    damaged_passport_allowed: bool | None

    temporary_passport_allowed: bool | None

    passport_issue_date_required: bool | None

    remarks: str | None

@dataclass
class TransitEvaluationResult:
    """
    Result produced by the Transit Evaluator.
    """

    transit_visa_required: bool

    airside_transit_allowed: bool

    baggage_collection_required: bool

    overnight_transit_allowed: bool

    max_transit_hours: int | None

    remarks: str | None
@dataclass
class VaccineRequirement:
    """
    Vaccine requirement associated with a health rule.
    """

    vaccine_name: str

    certificate_required: bool


@dataclass
class HealthEvaluationResult:
    """
    Result produced by the Health Evaluator.
    """

    health_form_required: bool

    quarantine_required: bool

    quarantine_days: int | None

    medical_certificate_required: bool

    vaccines: list[VaccineRequirement]

    remarks: str | None
@dataclass
class ImmigrationEvaluationResult:
    """
    Result produced by the Immigration Evaluator.
    """

    onward_ticket_required: bool

    accommodation_proof_required: bool

    proof_of_funds_required: bool

    biometric_required: bool

    interview_required: bool

    arrival_card_required: bool

    digital_arrival_card: bool

    arrival_registration_required: bool

    remarks: str | None
@dataclass
class CustomsEvaluationResult:
    """
    Result produced by the Customs Evaluator.
    """

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
@dataclass
class EntryRestrictionEvaluationResult:
    """
    Result produced by the Entry Restriction Evaluator.
    """

    restriction_type: str

    reason: str | None

    effective_date: date

    expiry_date: date | None

    source: str | None

    remarks: str | None

@dataclass
class RuleEngineResult:
    """
    Final result produced by the Rule Engine.
    """

    visa: VisaEvaluationResult | None

    passport: PassportEvaluationResult | None = None

    transit: TransitEvaluationResult | None = None

    health: HealthEvaluationResult | None = None

    immigration: ImmigrationEvaluationResult | None = None

    customs: CustomsEvaluationResult | None = None

    entry_restriction: EntryRestrictionEvaluationResult | None = None

@dataclass
class ComplianceDecision:
    """
    Final compliance decision returned by the Rule Engine.
    """

    status: str

    summary: str

    requirements: list[str]

    warnings: list[str]

    blockers: list[str]
