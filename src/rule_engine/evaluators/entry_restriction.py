from src.exceptions.rule_engine.no_matching_rule import (
    NoMatchingRuleError,
)
from src.rule_engine.models import (
    EntryRestrictionEvaluationResult,
    LoadedRules,
)


class EntryRestrictionEvaluator:
    """
    Evaluates entry restrictions applicable to the traveller.
    """

    def evaluate(
        self,
        rules: LoadedRules,
    ) -> EntryRestrictionEvaluationResult:

        entry_restriction = rules.entry_restriction

        if entry_restriction is None:
            raise NoMatchingRuleError("entry restriction")

        return EntryRestrictionEvaluationResult(
            restriction_type=entry_restriction.restriction_type,
            reason=entry_restriction.reason,
            effective_date=entry_restriction.effective_date,
            expiry_date=entry_restriction.expiry_date,
            source=(
                entry_restriction.source.authority_name
                if entry_restriction.source
                else None
            ),
            remarks=entry_restriction.remarks,
        )