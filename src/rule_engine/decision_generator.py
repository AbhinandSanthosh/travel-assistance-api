from datetime import datetime, timezone

from src.domain.decisions import (
    DecisionStatus,
    JourneySummary,
    Requirement,
    RequirementCategory,
    RequirementStatus,
    RuleExecutionRecord,
    TravelRequirementsDecision,
)
from src.rule_engine.models import (
    ComplianceContext,
    RuleEngineResult,
)


class DecisionGenerator:
    """Generates the final TISCO decision from evaluated requirements."""

    def generate(
        self,
        engine_result: RuleEngineResult,
        context: ComplianceContext,
        rule_version: str,
        check_id: str,
        execution_records: list[RuleExecutionRecord]
        | None = None,
        journey_origin: str = "",
        journey_destination: str = "",
    ) -> TravelRequirementsDecision:

        all_requirements = engine_result.requirements
        all_warnings = engine_result.warnings

        decision = self._determine_decision(
            all_requirements,
        )
        summary = self._generate_summary(decision)

        transit_countries: list[str] = []
        for tp in context.transit_points:
            if (
                tp.country
                and tp.country not in transit_countries
            ):
                transit_countries.append(tp.country)

        return TravelRequirementsDecision(
            check_id=check_id,
            decision=decision,
            summary=summary,
            requirements=all_requirements,
            warnings=all_warnings,
            journey=JourneySummary(
                origin=journey_origin,
                destination=journey_destination,
                transit_countries=transit_countries,
            ),
            rule_execution_log=execution_records or [],
            evaluated_at=datetime.now(timezone.utc),
            rule_version=rule_version,
        )

    def _determine_decision(
        self,
        requirements: list[Requirement],
    ) -> DecisionStatus:

        has_entry_restriction = any(
            r.category
            == RequirementCategory.ENTRY_RESTRICTION
            and r.status == RequirementStatus.REQUIRED
            for r in requirements
        )
        if has_entry_restriction:
            return DecisionStatus.NOT_PERMITTED

        has_unknown = any(
            r.status == RequirementStatus.UNKNOWN
            for r in requirements
        )
        has_required = any(
            r.status == RequirementStatus.REQUIRED
            for r in requirements
        )
        has_conditional = any(
            r.status == RequirementStatus.CONDITIONAL
            for r in requirements
        )

        if has_unknown and has_required:
            return DecisionStatus.ACTION_REQUIRED
        if has_unknown:
            return DecisionStatus.UNKNOWN
        if has_required:
            return DecisionStatus.ACTION_REQUIRED
        if has_conditional:
            return DecisionStatus.CONDITIONAL
        return DecisionStatus.CLEAR

    def _generate_summary(
        self,
        decision: DecisionStatus,
    ) -> str:

        summaries = {
            DecisionStatus.CLEAR: (
                "Passenger meets all evaluated "
                "travel requirements."
            ),
            DecisionStatus.ACTION_REQUIRED: (
                "One or more travel requirements must be "
                "fulfilled before departure."
            ),
            DecisionStatus.NOT_PERMITTED: (
                "Travel is not permitted to the "
                "destination country."
            ),
            DecisionStatus.CONDITIONAL: (
                "Travel may be possible subject "
                "to conditions being met."
            ),
            DecisionStatus.UNKNOWN: (
                "Insufficient regulatory data to fully "
                "evaluate travel requirements."
            ),
        }
        return summaries.get(
            decision,
            "Travel requirements evaluation complete.",
        )