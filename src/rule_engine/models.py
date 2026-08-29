from dataclasses import dataclass, field
from datetime import date

from src.domain.passenger import Passenger
from src.domain.journey import Journey, TransitPoint
from src.domain.decisions import Requirement

from src.models.compliance.customs_rule import CustomsRule
from src.models.compliance.entry_restriction import EntryRestriction
from src.models.compliance.health_rule import HealthRule
from src.models.compliance.immigration_rule import ImmigrationRule
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.transit_rule import TransitRule
from src.models.compliance.visa_rule import VisaRule


@dataclass
class JourneyRequest:
    """Rich journey request received from the API."""

    passenger: Passenger
    journey: Journey


@dataclass
class NormalizedJourney:
    """Journey after resolving all airport codes to country/airport IDs."""

    nationality_country_id: int
    destination_country_id: int
    origin_country_id: int | None
    purpose_id: int
    passport_type_id: int
    travel_date: date
    transit_points: list[TransitPoint] = field(
        default_factory=list,
    )
    destination_airport_id: int | None = None
    origin_airport_id: int | None = None


@dataclass
class ComplianceContext:
    """Shared context passed to every evaluator."""

    nationality_country_id: int
    destination_country_id: int
    purpose_id: int
    passport_type_id: int
    travel_date: date
    origin_country_id: int | None = None
    passenger: Passenger | None = None
    transit_points: list[TransitPoint] = field(
        default_factory=list,
    )


@dataclass
class TransitRuleEntry:
    """A transit rule paired with the transit point it applies to."""

    transit_point: TransitPoint
    transit_rule: TransitRule | None


@dataclass
class LoadedRules:
    """All applicable rules loaded for a journey."""

    visa_rule: VisaRule | None
    passport_rule: PassportRule | None
    health_rule: HealthRule | None
    immigration_rule: ImmigrationRule | None
    customs_rule: CustomsRule | None
    entry_restriction: EntryRestriction | None
    transit_rules: list[TransitRuleEntry] = field(
        default_factory=list,
    )


@dataclass
class RuleEngineResult:
    """Final result produced by the Rule Engine.

    context/loaded_rules are included alongside requirements/warnings
    so a single engine.execute() call is enough for a caller to build
    a full response (decision + per-domain detail + audit trail)
    without re-running journey_analyzer/context_builder/rule_loader a
    second time -- that duplication is exactly what produced the
    stale, broken second pipeline in autocheck_service.py.
    """

    requirements: list[Requirement] = field(
        default_factory=list,
    )
    warnings: list[Requirement] = field(
        default_factory=list,
    )
    context: ComplianceContext | None = None
    loaded_rules: LoadedRules | None = None
