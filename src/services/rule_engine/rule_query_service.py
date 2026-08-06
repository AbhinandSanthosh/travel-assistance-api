from sqlalchemy.orm import Session

from src.models.compliance.visa_rule import VisaRule
from src.models.compliance.passport_rule import PassportRule
from src.models.compliance.transit_rule import TransitRule
from sqlalchemy.orm import joinedload
from src.models.compliance.health_rule import HealthRule
from src.models.compliance.health_rule_vaccine import (
    HealthRuleVaccine,
)
from src.models.compliance.immigration_rule import (
    ImmigrationRule,
)
from src.models.compliance.customs_rule import CustomsRule
from src.models.compliance.entry_restriction import EntryRestriction
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

    def get_health_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
    ) -> HealthRule | None:
        """
        Retrieve the applicable health rule together with
        its associated vaccines.
        """

        return (
            self.db.query(HealthRule)
            .options(
                joinedload(
                    HealthRule.health_rule_vaccines
                ).joinedload(
                    HealthRuleVaccine.vaccine
                    )
            )
            .filter(
                HealthRule.nationality_country_id
                == nationality_country_id,
                HealthRule.destination_country_id
                == destination_country_id,
            )
            .first()
        )

    def get_immigration_rule(
        self,
        destination_country_id: int,
    ) -> ImmigrationRule | None:
        """
        Retrieve the applicable immigration rule.
        """

        return (
            self.db.query(ImmigrationRule)
            .filter(
                ImmigrationRule.destination_country_id
                == destination_country_id,
            )
            .first()
        )

    def get_customs_rule(
        self,
        nationality_country_id: int,
        destination_country_id: int,
    ) -> CustomsRule | None:
        """
        Retrieve the applicable customs rule.
        """

        return (
            self.db.query(CustomsRule)
            .options(
                joinedload(CustomsRule.currency)
            )
            .filter(
                CustomsRule.nationality_country_id
                == nationality_country_id,
                CustomsRule.destination_country_id
                == destination_country_id,
            )
            .first()
        )

    def get_entry_restriction(
        self,
        nationality_country_id: int,
        destination_country_id: int,
    ) -> EntryRestriction | None:
        """
        Retrieve the applicable entry restriction.
        """

        return (
            self.db.query(EntryRestriction)
            .options(
                joinedload(EntryRestriction.source)
            )
            .filter(
                EntryRestriction.nationality_country_id
                == nationality_country_id,
                EntryRestriction.destination_country_id
                == destination_country_id,
            )
            .first()
        )