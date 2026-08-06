from src.exceptions.rule_engine.no_matching_rule import (
    NoMatchingRuleError,
)
from src.rule_engine.models import (
    HealthEvaluationResult,
    LoadedRules,
    VaccineRequirement,
)


class HealthEvaluator:
    """
    Evaluates health requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> HealthEvaluationResult:

        health_rule = rules.health_rule

        if health_rule is None:
            raise NoMatchingRuleError("health")

        vaccines = [
            VaccineRequirement(
                vaccine_name=vaccine.vaccine.vaccine_name,
                certificate_required=vaccine.certificate_required,
            )
            for vaccine in health_rule.health_rule_vaccines
        ]

        return HealthEvaluationResult(
            health_form_required=health_rule.health_form_required,
            quarantine_required=health_rule.quarantine_required,
            quarantine_days=health_rule.quarantine_days,
            medical_certificate_required=health_rule.medical_certificate_required,
            vaccines=vaccines,
            remarks=health_rule.remarks,
        )