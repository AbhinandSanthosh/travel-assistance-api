from sqlalchemy.orm import Session

from src.models.reference.country import Country
from src.models.reference.passport_type import PassportType
from src.models.reference.purpose import Purpose


class ReferenceResolver:
    """
    Resolves reference/master data into database entities.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_country(self, country_name: str) -> Country:
        country = (
            self.db.query(Country)
            .filter(Country.country_name == country_name)
            .first()
        )

        if country is None:
            raise ValueError(
                f"Unknown country: {country_name}"
            )

        return country

    def get_purpose(self, purpose_code: str) -> Purpose:
        purpose = (
            self.db.query(Purpose)
            .filter(Purpose.purpose_code == purpose_code)
            .first()
        )

        if purpose is None:
            raise ValueError(
                f"Unknown purpose: {purpose_code}"
            )

        return purpose

    def get_passport_type(
        self,
        passport_code: str,
    ) -> PassportType:

        passport = (
            self.db.query(PassportType)
            .filter(
                PassportType.passport_code
                == passport_code
            )
            .first()
        )

        if passport is None:
            raise ValueError(
                f"Unknown passport type: {passport_code}"
            )

        return passport