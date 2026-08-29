from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.models import ComplianceContext, LoadedRules


class EntryRestrictionEvaluator:
    """Evaluates entry restrictions."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        entry_restriction = rules.entry_restriction

        if entry_restriction is None:
            return []

        if (
            entry_restriction.restriction_type.upper()
            == "NONE"
        ):
            return []

        # A restriction row can have its own validity window, separate
        # from the rule VERSION's effective/expiry dates (already
        # enforced at query time in RuleQueryService) -- e.g. a
        # specific country ban that only runs March-June 2026, even
        # though the general entry-restriction rule has been
        # published since last year with no expiry. Without this, a
        # restriction that hasn't started yet, or has already lapsed,
        # would incorrectly block travel.
        if (
            entry_restriction.effective_date
            and entry_restriction.effective_date > context.travel_date
        ):
            return []

        if (
            entry_restriction.expiry_date
            and entry_restriction.expiry_date < context.travel_date
        ):
            return []

        return [
            Requirement(
                category=RequirementCategory.ENTRY_RESTRICTION,
                status=RequirementStatus.REQUIRED,
                title=(
                    f"Entry restriction: "
                    f"{entry_restriction.restriction_type}"
                ),
                details=(
                    entry_restriction.reason
                    or (
                        "Entry to the destination "
                        "country is restricted."
                    )
                ),
                applicable_rule_id=str(
                    entry_restriction.rule_id,
                ),
                applicable_rule_code=(
                    entry_restriction.rule.rule_code
                    if entry_restriction.rule
                    else None
                ),
                source=(
                    entry_restriction.source.authority_name
                    if entry_restriction.source
                    else None
                ),
                effective_from=(
                    entry_restriction.effective_date
                ),
                effective_until=(
                    entry_restriction.expiry_date
                ),
            )
        ]