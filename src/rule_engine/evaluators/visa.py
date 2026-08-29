from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.evaluators._shared import unknown_requirement
from src.rule_engine.models import ComplianceContext, LoadedRules


class VisaEvaluator:
    """Evaluates visa requirements."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        visa_rule = rules.visa_rule

        if visa_rule is None:
            return unknown_requirement(RequirementCategory.VISA, "Visa requirement")

        rule_id = str(visa_rule.rule_id)
        rule_code = (
            visa_rule.rule.rule_code
            if visa_rule.rule
            else None
        )
        source = (
            visa_rule.rule.source.authority_name
            if visa_rule.rule and visa_rule.rule.source
            else None
        )

        if not visa_rule.visa_required:
            return [
                Requirement(
                    category=RequirementCategory.VISA,
                    status=RequirementStatus.NOT_REQUIRED,
                    title="Visa not required",
                    details="No visa required for entry.",
                    applicable_rule_id=rule_id,
                    applicable_rule_code=rule_code,
                    source=source,
                )
            ]

        visa_name = (
            visa_rule.visa_type.visa_name
            if visa_rule.visa_type
            else "Visa"
        )

        reqs: list[Requirement] = [
            Requirement(
                category=RequirementCategory.VISA,
                status=RequirementStatus.REQUIRED,
                title=f"{visa_name} required",
                details=(
                    f"Passenger must obtain the appropriate "
                    f"{visa_name} before travel."
                ),
                applicable_rule_id=rule_id,
                applicable_rule_code=rule_code,
                source=source,
            )
        ]

        if visa_rule.visa_on_arrival:
            reqs.append(
                Requirement(
                    category=RequirementCategory.VISA,
                    status=RequirementStatus.CONDITIONAL,
                    title="Visa on arrival available",
                    details=(
                        "Visa can be obtained on arrival "
                        "at the destination."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if visa_rule.evisa_available:
            reqs.append(
                Requirement(
                    category=RequirementCategory.VISA,
                    status=RequirementStatus.CONDITIONAL,
                    title="e-Visa available",
                    details=(
                        "Electronic visa application is "
                        "available for this destination."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        return reqs