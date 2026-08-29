from src.domain.decisions import (
    Requirement,
    RequirementCategory,
    RequirementStatus,
)
from src.rule_engine.models import ComplianceContext, LoadedRules


class TransitEvaluator:
    """Evaluates transit requirements for EACH transit point independently."""

    def evaluate(
        self,
        rules: LoadedRules,
        context: ComplianceContext,
    ) -> list[Requirement]:

        if not rules.transit_rules:
            return []

        reqs: list[Requirement] = []

        for entry in rules.transit_rules:
            tp = entry.transit_point
            transit_rule = entry.transit_rule
            label = (
                f"{tp.airport} ({tp.country})"
                if tp.country
                else tp.airport
            )

            if transit_rule is None:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.TRANSIT,
                        status=RequirementStatus.UNKNOWN,
                        title=(
                            f"Transit requirements unknown "
                            f"at {label}"
                        ),
                        details=(
                            f"No transit rule data available for "
                            f"transit through {label}."
                        ),
                    )
                )
                continue

            rule_id = str(transit_rule.rule_id)
            rule_code = (
                transit_rule.rule.rule_code
                if transit_rule.rule
                else None
            )
            source = (
                transit_rule.rule.source.authority_name
                if transit_rule.rule
                and transit_rule.rule.source
                else None
            )

            if transit_rule.transit_visa_required:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.TRANSIT,
                        status=RequirementStatus.REQUIRED,
                        title=(
                            f"Transit visa required at {label}"
                        ),
                        details=(
                            f"A transit visa is required for "
                            f"connecting through {label}."
                        ),
                        applicable_rule_id=rule_id,
                        applicable_rule_code=rule_code,
                        source=source,
                    )
                )
            else:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.TRANSIT,
                        status=RequirementStatus.NOT_REQUIRED,
                        title=(
                            f"Transit visa not required "
                            f"at {label}"
                        ),
                        details=(
                            f"No transit visa needed when "
                            f"connecting through {label}."
                        ),
                        applicable_rule_id=rule_id,
                    )
                )

            if not transit_rule.airside_transit_allowed:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.TRANSIT,
                        status=RequirementStatus.REQUIRED,
                        title=(
                            f"Airside transit not permitted "
                            f"at {label}"
                        ),
                        details=(
                            f"Passengers must clear immigration "
                            f"when transiting through {label}."
                        ),
                        applicable_rule_id=rule_id,
                    )
                )

            if transit_rule.baggage_collection_required:
                reqs.append(
                    Requirement(
                        category=RequirementCategory.TRANSIT,
                        status=RequirementStatus.REQUIRED,
                        title=(
                            f"Baggage collection required "
                            f"at {label}"
                        ),
                        details=(
                            f"Passengers must collect and re-check "
                            f"baggage during transit at {label}."
                        ),
                        applicable_rule_id=rule_id,
                    )
                )

        return reqs