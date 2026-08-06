from src.exceptions.rule_engine.no_matching_rule import (
    NoMatchingRuleError,
)
from src.rule_engine.models import (
    CustomsEvaluationResult,
    LoadedRules,
)


class CustomsEvaluator:
    """
    Evaluates customs requirements.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> CustomsEvaluationResult:

        customs_rule = rules.customs_rule

        if customs_rule is None:
            raise NoMatchingRuleError("customs")

        return CustomsEvaluationResult(
            alcohol_limit=customs_rule.alcohol_limit,
            tobacco_limit=customs_rule.tobacco_limit,
            currency_limit_amount=customs_rule.currency_limit_amount,
            currency=(
                customs_rule.currency.currency_code
                if customs_rule.currency
                else None
            ),
            currency_declaration_required=(
                customs_rule.currency_declaration_required
            ),
            medication_rules=customs_rule.medication_rules,
            prohibited_items=customs_rule.prohibited_items,
            restricted_items=customs_rule.restricted_items,
            pet_import_rules=customs_rule.pet_import_rules,
            remarks=customs_rule.remarks,
        )