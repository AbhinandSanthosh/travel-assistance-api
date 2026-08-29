from datetime import date

from src.db.session import SessionLocal
from src.domain.journey import Journey
from src.domain.passenger import Passenger, PassportInfo
from src.rule_engine.engine import RuleEngine
from src.rule_engine.models import JourneyRequest, RuleEngineResult


def main() -> None:
    """
    Execute the Rule Engine manually -- exercises the SAME single
    engine.execute() path production traffic goes through (see
    AutoCheckService._run_rule_engine), just with a hand-built request
    instead of one parsed from an HTTP payload.
    """

    db = SessionLocal()

    try:
        passenger = Passenger(
            nationality="IN",
            passport=PassportInfo(
                issuing_country="IN",
                type="PP",
                valid_until=date(2027, 4, 15),
            ),
        )
        journey = Journey(
            origin="COK",
            destination="WAW",
            travel_date=date(2026, 9, 15),
            purpose="TOUR",
        )
        request = JourneyRequest(passenger=passenger, journey=journey)

        engine = RuleEngine(db)
        engine_result = engine.execute(request)

        decision = engine.decision_generator.generate(
            engine_result=RuleEngineResult(
                requirements=engine_result.requirements,
                warnings=engine_result.warnings,
            ),
            context=engine_result.context,
            rule_version="manual-test",
            check_id="chk_manual_test",
            journey_origin=journey.origin,
            journey_destination=journey.destination,
        )

        print("\n========== RULE ENGINE RESULT ==========\n")

        print("Requirements")
        print("------------")
        for req in engine_result.requirements:
            print(f"  [{req.category.value}] {req.status.value}: {req.title}")

        print("\nWarnings")
        print("--------")
        for req in engine_result.warnings:
            print(f"  [{req.category.value}] {req.status.value}: {req.title}")

        print("\nDecision")
        print("--------")
        print(f"  {decision.decision.value}: {decision.summary}")

        print("\n========================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
