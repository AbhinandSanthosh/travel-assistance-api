from src.rule_engine.models import (
    LoadedRules,
    TransitEvaluationResult,
)


class TransitEvaluator:
    """
    Evaluates transit requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> TransitEvaluationResult | None:

        transit_rule = rules.transit_rule

        if transit_rule is None:
            return None

        return TransitEvaluationResult(
            transit_visa_required=transit_rule.transit_visa_required,
            airside_transit_allowed=transit_rule.airside_transit_allowed,
            baggage_collection_required=transit_rule.baggage_collection_required,
            overnight_transit_allowed=transit_rule.overnight_transit_allowed,
            max_transit_hours=transit_rule.max_transit_hours,
            remarks=transit_rule.remarks,
        )