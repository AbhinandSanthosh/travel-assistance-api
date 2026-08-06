from datetime import date

from sqlalchemy.orm import Session

from src.rule_engine.context_builder import ContextBuilder
from src.rule_engine.evaluators.visa import VisaEvaluator
from src.rule_engine.journey_analyzer import JourneyAnalyzer

from src.rule_engine.models import (
    JourneyRequest,
    RuleEngineResult,
)
from src.rule_engine.evaluators.passport import PassportEvaluator
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

    def execute(
        self,
        request: JourneyRequest,
    ) -> RuleEngineResult:
        """
        Execute the Visa Rule Engine pipeline.
        """

        journey = self.journey_analyzer.analyze(request)

        context = self.context_builder.build(
            journey=journey,
            travel_date=date.today(),
        )

        loaded_rules = self.rule_loader.load(context)

        visa_result = self.visa_evaluator.evaluate(
            loaded_rules,
        )

        passport_result = self.passport_evaluator.evaluate(
            loaded_rules,
        )

        return RuleEngineResult(
            visa=visa_result,
            passport=passport_result,
        )