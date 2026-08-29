from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.evaluators._shared import unknown_requirement
from src.rule_engine.models import ComplianceContext, LoadedRules


class ImmigrationEvaluator:
    """Evaluates immigration requirements."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        immigration_rule = rules.immigration_rule

        if immigration_rule is None:
            return unknown_requirement(RequirementCategory.IMMIGRATION, "Immigration requirements")

        rule_id = str(immigration_rule.rule_id)
        rule_code = (
            immigration_rule.rule.rule_code
            if immigration_rule.rule
            else None
        )
        source = (
            immigration_rule.rule.source.authority_name
            if immigration_rule.rule
            and immigration_rule.rule.source
            else None
        )

        reqs: list[Requirement] = []

        field_map = [
            (
                immigration_rule.onward_ticket_required,
                "Onward/return ticket",
                "Carry proof of onward or return travel.",
            ),
            (
                immigration_rule.accommodation_proof_required,
                "Proof of accommodation",
                (
                    "Carry proof of accommodation for "
                    "the duration of stay."
                ),
            ),
            (
                immigration_rule.proof_of_funds_required,
                "Proof of sufficient funds",
                (
                    "Carry proof of sufficient "
                    "financial means."
                ),
            ),
            (
                immigration_rule.biometric_required,
                "Biometric verification",
                (
                    "Biometric data collection "
                    "required on arrival."
                ),
            ),
            (
                immigration_rule.interview_required,
                "Immigration interview",
                "An immigration interview may be required.",
            ),
            (
                immigration_rule.arrival_card_required,
                "Arrival card",
                (
                    "Complete the arrival/"
                    "disembarkation card."
                ),
            ),
            (
                immigration_rule.arrival_registration_required,
                "Arrival registration",
                (
                    "Register with local authorities "
                    "after arrival."
                ),
            ),
        ]

        for required, title, details in field_map:
            if required:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.IMMIGRATION,
                        status=RequirementStatus.REQUIRED,
                        title=title,
                        details=details,
                        applicable_rule_id=rule_id,
                        applicable_rule_code=rule_code,
                        source=source,
                    )
                )

        if immigration_rule.digital_arrival_card:
            reqs.append(
                Requirement(
                    category=RequirementCategory.IMMIGRATION,
                    status=RequirementStatus.RECOMMENDED,
                    title="Digital arrival card available",
                    details=(
                        "A digital/electronic arrival card "
                        "option is available."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if not reqs:
            reqs.append(
                Requirement(
                    category=RequirementCategory.IMMIGRATION,
                    status=RequirementStatus.NOT_REQUIRED,
                    title="Standard immigration procedures",
                    details=(
                        "No special immigration requirements "
                        "beyond standard entry procedures."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        return reqs