from datetime import date

from sqlalchemy.orm import Session

from src.rule_engine.context_builder import ContextBuilder
from src.rule_engine.decision_generator import (
    DecisionGenerator,
)
from src.rule_engine.evaluators.customs import (
    CustomsEvaluator,
)
from src.rule_engine.evaluators.entry_restriction import (
    EntryRestrictionEvaluator,
)
from src.rule_engine.evaluators.health import (
    HealthEvaluator,
)
from src.rule_engine.evaluators.immigration import (
    ImmigrationEvaluator,
)
from src.rule_engine.evaluators.passport import (
    PassportEvaluator,
)
from src.rule_engine.evaluators.transit import (
    TransitEvaluator,
)
from src.rule_engine.evaluators.visa import (
    VisaEvaluator,
)
from src.rule_engine.journey_analyzer import JourneyAnalyzer
from src.rule_engine.models import (
    JourneyRequest,
    RuleEngineResult,
)
from src.rule_engine.rule_loader import RuleLoader


class RuleEngine:
    """
    Orchestrates the execution of the Rule Engine.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

        self.journey_analyzer = JourneyAnalyzer(db)
        self.context_builder = ContextBuilder()
        self.rule_loader = RuleLoader(db)

        self.visa_evaluator = VisaEvaluator()
        self.passport_evaluator = PassportEvaluator()
        self.transit_evaluator = TransitEvaluator()
        self.health_evaluator = HealthEvaluator()
        self.immigration_evaluator = ImmigrationEvaluator()
        self.customs_evaluator = CustomsEvaluator()
        self.entry_restriction_evaluator = (
            EntryRestrictionEvaluator()
        )

        self.decision_generator = DecisionGenerator()

    def execute(
        self,
        request: JourneyRequest,
    ) -> RuleEngineResult:
        """
        Execute the complete Rule Engine pipeline.
        """

        journey = self.journey_analyzer.analyze(
            request,
        )

        context = self.context_builder.build(
            journey=journey,
            travel_date=date.today(),
        )

        loaded_rules = self.rule_loader.load(
            context,
        )

        visa_result = self.visa_evaluator.evaluate(
            loaded_rules,
        )

        passport_result = self.passport_evaluator.evaluate(
            loaded_rules,
        )

        transit_result = self.transit_evaluator.evaluate(
            loaded_rules,
        )

        health_result = self.health_evaluator.evaluate(
            loaded_rules,
        )

        immigration_result = (
            self.immigration_evaluator.evaluate(
                loaded_rules,
            )
        )

        customs_result = (
            self.customs_evaluator.evaluate(
                loaded_rules,
            )
        )

        entry_restriction_result = (
            self.entry_restriction_evaluator.evaluate(
                loaded_rules,
            )
        )

        rule_engine_result = RuleEngineResult(
            visa=visa_result,
            passport=passport_result,
            transit=transit_result,
            health=health_result,
            immigration=immigration_result,
            customs=customs_result,
            entry_restriction=entry_restriction_result,
        )

        # Generate the final compliance decision.
        # We are not returning it yet.
        self.decision_generator.generate(
            rule_engine_result,
        )

        return rule_engine_result