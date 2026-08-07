from sqlalchemy import func, or_
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
            .filter(func.lower(Country.country_name) == country_name.strip().lower())
            .first()
        )

        if country is None:
            valid_names = sorted(
                c.country_name for c in self.db.query(Country).all()
            )
            raise ValueError(
                f"Unknown country: {country_name}. "
                f"Valid country names: {', '.join(valid_names)}"
            )

        return country

    def get_purpose(self, purpose: str) -> Purpose:
        normalized = purpose.strip().lower()

        match = (
            self.db.query(Purpose)
            .filter(
                or_(
                    func.lower(Purpose.purpose_code) == normalized,
                    func.lower(Purpose.purpose_name) == normalized,
                )
            )
            .first()
        )

        if match is None:
            valid_codes = sorted(
                p.purpose_code for p in self.db.query(Purpose).all()
            )
            raise ValueError(
                f"Unknown purpose: {purpose}. "
                f"Valid purpose codes: {', '.join(valid_codes)}"
            )

        return match

    def get_passport_type(
        self,
        passport_type: str,
    ) -> PassportType:
        normalized = passport_type.strip().lower()

        match = (
            self.db.query(PassportType)
            .filter(
                or_(
                    func.lower(PassportType.passport_code) == normalized,
                    func.lower(PassportType.passport_name) == normalized,
                )
            )
            .first()
        )

        if match is None:
            valid_codes = sorted(
                p.passport_code for p in self.db.query(PassportType).all()
            )
            raise ValueError(
                f"Unknown passport type: {passport_type}. "
                f"Valid passport type codes: {', '.join(valid_codes)}"
            )

        return match