from sqlalchemy.orm import Session

from src.models.reference.passenger_type import PassengerType
from src.repositories.base_repository import BaseRepository


class PassengerTypeRepository(BaseRepository[PassengerType]):
    """Repository for PassengerType operations."""

    def __init__(self):
        super().__init__(PassengerType)

    def get_by_code(
        self,
        db: Session,
        passenger_type_code: str,
    ) -> PassengerType | None:
        """Retrieve a passenger type by code."""

        return (
            db.query(PassengerType)
            .filter(
                PassengerType.passenger_type_code == passenger_type_code,
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        passenger_type_name: str,
    ) -> PassengerType | None:
        """Retrieve a passenger type by name."""

        return (
            db.query(PassengerType)
            .filter(
                PassengerType.passenger_type_name == passenger_type_name,
            )
            .first()
        )