from src.rule_engine.models import (
    LoadedRules,
    VisaEvaluationResult,
)

class VisaEvaluator:
    """
    Evaluates visa requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> VisaEvaluationResult | None:

        visa_rule = rules.visa_rule

        if visa_rule is None:
            return None

        return VisaEvaluationResult(
            visa_required=visa_rule.visa_required,
            visa_type=visa_rule.visa_type.visa_name,
            visa_on_arrival=visa_rule.visa_on_arrival,
            evisa_available=visa_rule.evisa_available,
            max_stay_days=visa_rule.max_stay_days,
            multiple_entry=visa_rule.multiple_entry,
            remarks=visa_rule.remarks,
        )