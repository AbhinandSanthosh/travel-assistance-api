from src.rule_engine.models import (
    ImmigrationEvaluationResult,
    LoadedRules,
)


class ImmigrationEvaluator:
    """
    Evaluates immigration requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> ImmigrationEvaluationResult | None:

        immigration_rule = rules.immigration_rule

        if immigration_rule is None:
            return None

        return ImmigrationEvaluationResult(
            onward_ticket_required=immigration_rule.onward_ticket_required,
            accommodation_proof_required=(
                immigration_rule.accommodation_proof_required
            ),
            proof_of_funds_required=(
                immigration_rule.proof_of_funds_required
            ),
            biometric_required=(
                immigration_rule.biometric_required
            ),
            interview_required=(
                immigration_rule.interview_required
            ),
            arrival_card_required=(
                immigration_rule.arrival_card_required
            ),
            digital_arrival_card=(
                immigration_rule.digital_arrival_card
            ),
            arrival_registration_required=(
                immigration_rule.arrival_registration_required
            ),
            remarks=immigration_rule.remarks,
        )