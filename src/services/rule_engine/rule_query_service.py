from sqlalchemy.orm import Session

from src.models.compliance.visa_rule import VisaRule
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.transit_rule import TransitRule
class RuleQueryService:
    """
    Read-only queries used by the Rule Engine.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_visa_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        passport_type_id: int,
        purpose_id: int,
    ) -> VisaRule | None:
        """
        Retrieve the applicable visa rule.
        """

        return (
            self.db.query(VisaRule)
            .filter(
                VisaRule.nationality_country_id
                == nationality_country_id,
                VisaRule.destination_country_id
                == destination_country_id,
                VisaRule.passport_type_id
                == passport_type_id,
                VisaRule.purpose_id
                == purpose_id,
            )
            .first()
        )

    def get_passport_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
        passport_type_id: int,
    ) -> PassportRule | None:
        """
        Retrieve the applicable passport rule.
        """

        return (
            self.db.query(PassportRule)
            .filter(
                PassportRule.destination_country_id
                == destination_country_id,
                PassportRule.passport_type_id
                == passport_type_id,
            )
            .first()
        )

    

    def get_transit_rule(
        self,
        nationality_country_id: int,
        transit_country_id: int,
        transit_airport_id: int,
    ) -> TransitRule | None:
        """
        Retrieve the applicable transit rule.
        """

        return (
            self.db.query(TransitRule)
            .filter(
                TransitRule.nationality_country_id
                == nationality_country_id,
                TransitRule.transit_country_id
                == transit_country_id,
                TransitRule.transit_airport_id
                == transit_airport_id,
            )
            .first()
        )