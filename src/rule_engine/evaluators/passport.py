from src.rule_engine.models import (
    LoadedRules,
    PassportEvaluationResult,
)



class PassportEvaluator:
    """
    Evaluates passport requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> PassportEvaluationResult | None:

        passport_rule = rules.passport_rule

        if passport_rule is None:
            return None

        return PassportEvaluationResult(
            minimum_validity_months=passport_rule.minimum_validity_months,
            blank_pages_required=passport_rule.blank_pages_required,
            machine_readable_required=passport_rule.machine_readable_required,
            damaged_passport_allowed=passport_rule.damaged_passport_allowed,
            temporary_passport_allowed=passport_rule.temporary_passport_allowed,
            passport_issue_date_required=passport_rule.passport_issue_date_required,
            remarks=passport_rule.remarks,
        )