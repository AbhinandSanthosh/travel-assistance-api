from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.evaluators._shared import unknown_requirement
from src.rule_engine.models import ComplianceContext, LoadedRules


class CustomsEvaluator:
    """Evaluates customs requirements."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        customs_rule = rules.customs_rule

        if customs_rule is None:
            return unknown_requirement(RequirementCategory.CUSTOMS, "Customs requirements")

        rule_id = str(customs_rule.rule_id)
        reqs: list[Requirement] = []

        if customs_rule.currency_declaration_required:
            limit_info = ""
            if (
                customs_rule.currency_limit_amount
                and customs_rule.currency
            ):
                code = customs_rule.currency.currency_code
                limit_info = (
                    f" exceeding "
                    f"{customs_rule.currency_limit_amount} "
                    f"{code}"
                )
            reqs.append(
                Requirement(
                    category=RequirementCategory.CUSTOMS,
                    status=RequirementStatus.REQUIRED,
                    title="Currency declaration",
                    details=(
                        f"Declare currency{limit_info} "
                        f"when entering the country."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if customs_rule.medication_rules:
            reqs.append(
                Requirement(
                    category=RequirementCategory.CUSTOMS,
                    status=RequirementStatus.RECOMMENDED,
                    title="Medication import rules",
                    details=(
                        f"Prescription medicines: "
                        f"{customs_rule.medication_rules}"
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if customs_rule.prohibited_items:
            reqs.append(
                Requirement(
                    category=RequirementCategory.CUSTOMS,
                    status=RequirementStatus.REQUIRED,
                    title="Prohibited items",
                    details=(
                        f"The following items are prohibited: "
                        f"{customs_rule.prohibited_items}"
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if not reqs:
            reqs.append(
                Requirement(
                    category=RequirementCategory.CUSTOMS,
                    status=RequirementStatus.NOT_REQUIRED,
                    title="Standard customs procedures",
                    details="No special customs requirements.",
                    applicable_rule_id=rule_id,
                )
            )

        return reqs