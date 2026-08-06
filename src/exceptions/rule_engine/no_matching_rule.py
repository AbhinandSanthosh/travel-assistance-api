from src.exceptions.rule_engine.base import (
    RuleEngineError,
)


class NoMatchingRuleError(RuleEngineError):
    """
    Raised when no applicable rule exists
    for the supplied traveller context.
    """

    def __init__(
        self,
        rule_type: str,
    ) -> None:
        self.rule_type = rule_type

        super().__init__(
            f"No matching {rule_type} rule found."
        )