from sqlalchemy.orm import Session

from src.models.reference.travel_authorization import TravelAuthorization
from src.repositories.base_repository import BaseRepository


class TravelAuthorizationRepository(
    BaseRepository[TravelAuthorization],
):
    """Repository for TravelAuthorization operations."""

    def __init__(self):
        super().__init__(TravelAuthorization)

    def get_by_code(
        self,
        db: Session,
        authorization_code: str,
    ) -> TravelAuthorization | None:
        """Retrieve a travel authorization by code."""

        return (
            db.query(TravelAuthorization)
            .filter(
                TravelAuthorization.authorization_code
                == authorization_code,
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        authorization_name: str,
    ) -> TravelAuthorization | None:
        """Retrieve a travel authorization by name."""

        return (
            db.query(TravelAuthorization)
            .filter(
                TravelAuthorization.authorization_name
                == authorization_name,
            )
            .first()
        )