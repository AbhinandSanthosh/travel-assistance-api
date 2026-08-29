from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
    SubRequirement,
)
from src.rule_engine.evaluators._shared import unknown_requirement
from src.rule_engine.models import ComplianceContext, LoadedRules


class HealthEvaluator:
    """Evaluates health requirements with structured vaccine sub-requirements."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        health_rule = rules.health_rule

        if health_rule is None:
            return unknown_requirement(RequirementCategory.HEALTH, "Health requirements")

        rule_id = str(health_rule.rule_id)
        rule_code = (
            health_rule.rule.rule_code
            if health_rule.rule
            else None
        )
        source = (
            health_rule.rule.source.authority_name
            if health_rule.rule and health_rule.rule.source
            else None
        )

        reqs: list[Requirement] = []

        # Vaccine sub-requirements
        sub_reqs: list[SubRequirement] = []

        for hrv in health_rule.health_rule_vaccines:
            vaccine_name = hrv.vaccine.vaccine_name
            sub_reqs.append(
                SubRequirement(
                    type="VACCINATION",
                    name=vaccine_name,
                    status=(
                        RequirementStatus.REQUIRED
                        if hrv.certificate_required
                        else RequirementStatus.RECOMMENDED
                    ),
                    details=(
                        f"{vaccine_name} vaccination "
                        f"{'certificate required' if hrv.certificate_required else 'recommended'}."
                    ),
                )
            )

        if sub_reqs:
            reqs.append(
                Requirement(
                    category=RequirementCategory.HEALTH,
                    status=RequirementStatus.REQUIRED,
                    title="Vaccination requirements",
                    details=(
                        "One or more vaccinations are "
                        "required or recommended."
                    ),
                    sub_requirements=sub_reqs,
                    applicable_rule_id=rule_id,
                    applicable_rule_code=rule_code,
                    source=source,
                )
            )

        if health_rule.health_form_required:
            reqs.append(
                Requirement(
                    category=RequirementCategory.HEALTH,
                    status=RequirementStatus.REQUIRED,
                    title="Health declaration form",
                    details=(
                        "Complete the required health "
                        "declaration form before travel."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if health_rule.quarantine_required:
            days = (
                f" ({health_rule.quarantine_days} days)"
                if health_rule.quarantine_days
                else ""
            )
            reqs.append(
                Requirement(
                    category=RequirementCategory.HEALTH,
                    status=RequirementStatus.REQUIRED,
                    title="Quarantine required",
                    details=(
                        f"Mandatory quarantine period "
                        f"on arrival{days}."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if health_rule.medical_certificate_required:
            reqs.append(
                Requirement(
                    category=RequirementCategory.HEALTH,
                    status=RequirementStatus.REQUIRED,
                    title="Medical certificate required",
                    details=(
                        "A valid medical certificate "
                        "must be carried."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if not reqs:
            reqs.append(
                Requirement(
                    category=RequirementCategory.HEALTH,
                    status=RequirementStatus.NOT_REQUIRED,
                    title="No health requirements",
                    details=(
                        "No specific health requirements "
                        "for this route."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        return reqs