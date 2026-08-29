from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.evaluators._shared import unknown_requirement
from src.rule_engine.models import ComplianceContext, LoadedRules


class PassportEvaluator:
    """Evaluates passport requirements."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        passport_rule = rules.passport_rule

        if passport_rule is None:
            return unknown_requirement(RequirementCategory.PASSPORT, "Passport requirements")

        rule_id = str(passport_rule.rule_id)
        rule_code = (
            passport_rule.rule.rule_code
            if passport_rule.rule
            else None
        )
        source = (
            passport_rule.rule.source.authority_name
            if passport_rule.rule and passport_rule.rule.source
            else None
        )

        reqs: list[Requirement] = []

        if passport_rule.minimum_validity_months:
            reqs.append(
                Requirement(
                    category=RequirementCategory.PASSPORT,
                    status=RequirementStatus.REQUIRED,
                    title="Passport validity",
                    details=(
                        f"Passport must be valid for at least "
                        f"{passport_rule.minimum_validity_months} "
                        f"months from travel date."
                    ),
                    applicable_rule_id=rule_id,
                    applicable_rule_code=rule_code,
                    source=source,
                )
            )

        if passport_rule.blank_pages_required:
            reqs.append(
                Requirement(
                    category=RequirementCategory.PASSPORT,
                    status=RequirementStatus.REQUIRED,
                    title="Blank pages required",
                    details=(
                        f"Passport must contain at least "
                        f"{passport_rule.blank_pages_required} "
                        f"blank pages."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if passport_rule.machine_readable_required:
            reqs.append(
                Requirement(
                    category=RequirementCategory.PASSPORT,
                    status=RequirementStatus.REQUIRED,
                    title="Machine-readable passport required",
                    details=(
                        "Passport must be machine-readable "
                        "(MRP/MRTD)."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if passport_rule.temporary_passport_allowed is False:
            reqs.append(
                Requirement(
                    category=RequirementCategory.PASSPORT,
                    status=RequirementStatus.REQUIRED,
                    title="Temporary passport not accepted",
                    details=(
                        "Temporary/emergency passports are "
                        "not accepted for entry."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        if not reqs:
            reqs.append(
                Requirement(
                    category=RequirementCategory.PASSPORT,
                    status=RequirementStatus.NOT_REQUIRED,
                    title="Standard passport accepted",
                    details=(
                        "No special passport requirements "
                        "beyond a valid travel document."
                    ),
                    applicable_rule_id=rule_id,
                )
            )

        return reqs