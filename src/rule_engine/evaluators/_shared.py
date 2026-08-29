from src.domain.decisions import Requirement, RequirementCategory, RequirementStatus


def unknown_requirement(category: RequirementCategory, subject: str) -> list[Requirement]:
    """The shared 'no rule data found for this combination' fallback.

    Deliberately returns UNKNOWN, never NOT_REQUIRED -- a compliance
    system must never let missing regulatory data silently present as
    "you're clear." Used by every evaluator except EntryRestriction
    (where "no row" legitimately means "no restriction exists", not
    "unknown") and Transit (whose fallback needs a per-transit-point
    label, not just a category).
    """

    return [
        Requirement(
            category=category,
            status=RequirementStatus.UNKNOWN,
            title=f"{subject} unknown",
            details=f"No {subject.lower()} data available for this combination.",
        )
    ]
