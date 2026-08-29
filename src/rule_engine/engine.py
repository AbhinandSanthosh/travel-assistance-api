from sqlalchemy.orm import Session

from src.domain.decisions import RequirementStatus
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
from src.rule_engine.evaluators.health import HealthEvaluator
from src.rule_engine.evaluators.immigration import (
    ImmigrationEvaluator,
)
from src.rule_engine.evaluators.passport import (
    PassportEvaluator,
)
from src.rule_engine.evaluators.transit import (
    TransitEvaluator,
)
from src.rule_engine.evaluators.visa import VisaEvaluator
from src.rule_engine.journey_analyzer import JourneyAnalyzer
from src.rule_engine.models import (
    JourneyRequest,
    RuleEngineResult,
)
from src.rule_engine.rule_loader import RuleLoader


class RuleEngine:
    """Orchestrates the TISCO Decision Engine pipeline."""

    def __init__(self, db: Session) -> None:
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
        self, request: JourneyRequest,
    ) -> RuleEngineResult:
        """Execute the complete TISCO Decision Engine pipeline."""

        journey = self.journey_analyzer.analyze(request)

        context = self.context_builder.build(
            journey=journey,
            passenger=request.passenger,
        )

        loaded_rules = self.rule_loader.load(context)

        requirements = []
        warnings = []

        # Entry restrictions first (highest priority)
        requirements.extend(
            self.entry_restriction_evaluator.evaluate(
                loaded_rules,
                context,
            )
        )

        # Destination evaluations
        requirements.extend(
            self.visa_evaluator.evaluate(
                loaded_rules, context,
            )
        )
        requirements.extend(
            self.passport_evaluator.evaluate(
                loaded_rules, context,
            )
        )
        requirements.extend(
            self.health_evaluator.evaluate(
                loaded_rules, context,
            )
        )
        requirements.extend(
            self.immigration_evaluator.evaluate(
                loaded_rules, context,
            )
        )

        # Transit evaluations (per transit point)
        requirements.extend(
            self.transit_evaluator.evaluate(
                loaded_rules, context,
            )
        )

        # Customs — RECOMMENDED → warnings, REQUIRED → reqs
        for req in self.customs_evaluator.evaluate(
            loaded_rules,
            context,
        ):
            if req.status in (
                RequirementStatus.RECOMMENDED,
                RequirementStatus.NOT_REQUIRED,
            ):
                warnings.append(req)
            else:
                requirements.append(req)

        return RuleEngineResult(
            requirements=requirements,
            warnings=warnings,
            context=context,
            loaded_rules=loaded_rules,
        )