from src.db.session import SessionLocal
from src.rule_engine.engine import RuleEngine
from src.rule_engine.models import JourneyRequest


def main() -> None:
    """
    Execute the Rule Engine manually.
    """

    db = SessionLocal()

    try:
        request = JourneyRequest(
            nationality="India",
            destination="Poland",
            purpose="TOUR",
            passport_type="PP",
        )

        engine = RuleEngine(db)

        result = engine.execute(request)

        print("\n========== RULE ENGINE RESULT ==========\n")

        print("Visa Evaluation")
        print("----------------")
        print(result.visa)

        print("\nPassport Evaluation")
        print("-------------------")
        print(result.passport)

        print("\nTransit Evaluation")
        print("------------------")
        print(result.transit)

        print("\nHealth Evaluation")
        print("-----------------")
        print(result.health)

        print("\nImmigration Evaluation")
        print("----------------------")
        print(result.immigration)

        print("\nCustoms Evaluation")
        print("------------------")
        print(result.customs)

        print("\nEntry Restriction Evaluation")
        print("----------------------------")
        print(result.entry_restriction)

        print("\n========================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()