from sqlalchemy.orm import Session

from src.models.reference.purpose import Purpose
from src.repositories.base_repository import BaseRepository


class PurposeRepository(BaseRepository[Purpose]):
    """Repository for Purpose operations."""

    def __init__(self):
        super().__init__(Purpose)

    def get_by_code(
        self,
        db: Session,
        purpose_code: str,
    ) -> Purpose | None:
        """Retrieve a purpose by code."""

        return (
            db.query(Purpose)
            .filter(
                Purpose.purpose_code == purpose_code,
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        purpose_name: str,
    ) -> Purpose | None:
        """Retrieve a purpose by name."""

        return (
            db.query(Purpose)
            .filter(
                Purpose.purpose_name == purpose_name,
            )
            .first()
        )