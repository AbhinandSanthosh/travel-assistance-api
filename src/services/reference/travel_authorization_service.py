from sqlalchemy.orm import Session

from src.exceptions.country import CountryNotFoundError
from src.exceptions.travel_authorization import (
    TravelAuthorizationAlreadyExistsError,
    TravelAuthorizationNotFoundError,
)
from src.models.reference.travel_authorization import (
    TravelAuthorization,
)
from src.repositories.reference.country_repository import CountryRepository
from src.repositories.reference.travel_authorization_repository import (
    TravelAuthorizationRepository,
)
from src.schemas.reference.travel_authorization import (
    TravelAuthorizationCreate,
    TravelAuthorizationUpdate,
)


class TravelAuthorizationService:
    """Service layer for TravelAuthorization."""

    def __init__(
        self,
        travel_authorization_repository: TravelAuthorizationRepository,
        country_repository: CountryRepository,
    ):
        self.travel_authorization_repository = (
            travel_authorization_repository
        )
        self.country_repository = country_repository

    def create_travel_authorization(
        self,
        db: Session,
        travel_authorization_data: TravelAuthorizationCreate,
    ) -> TravelAuthorization:
        """Create a travel authorization."""

        existing_code = (
            self.travel_authorization_repository.get_by_code(
                db,
                travel_authorization_data.authorization_code,
            )
        )
        if existing_code:
            raise TravelAuthorizationAlreadyExistsError(
                "authorization_code",
                travel_authorization_data.authorization_code,
            )

        existing_name = (
            self.travel_authorization_repository.get_by_name(
                db,
                travel_authorization_data.authorization_name,
            )
        )
        if existing_name:
            raise TravelAuthorizationAlreadyExistsError(
                "authorization_name",
                travel_authorization_data.authorization_name,
            )

        country = self.country_repository.get_by_id(
            db,
            travel_authorization_data.destination_country_id,
        )
        if not country:
            raise CountryNotFoundError(
                travel_authorization_data.destination_country_id,
            )

        travel_authorization = TravelAuthorization(
            **travel_authorization_data.model_dump(),
        )

        return self.travel_authorization_repository.create(
            db,
            travel_authorization,
        )

    def get_travel_authorization(
        self,
        db: Session,
        travel_authorization_id: int,
    ) -> TravelAuthorization:
        """Get a travel authorization by ID."""

        travel_authorization = (
            self.travel_authorization_repository.get_by_id(
                db,
                travel_authorization_id,
            )
        )

        if not travel_authorization:
            raise TravelAuthorizationNotFoundError(
                travel_authorization_id,
            )

        return travel_authorization

    def get_all_travel_authorizations(
        self,
        db: Session,
    ) -> list[TravelAuthorization]:
        """Get all travel authorizations."""

        return self.travel_authorization_repository.get_all(db)

    def update_travel_authorization(
        self,
        db: Session,
        travel_authorization_id: int,
        travel_authorization_data: TravelAuthorizationUpdate,
    ) -> TravelAuthorization:
        """Update a travel authorization."""

        travel_authorization = (
            self.travel_authorization_repository.get_by_id(
                db,
                travel_authorization_id,
            )
        )

        if not travel_authorization:
            raise TravelAuthorizationNotFoundError(
                travel_authorization_id,
            )

        update_data = travel_authorization_data.model_dump(
            exclude_unset=True,
        )

        if (
            "authorization_code" in update_data
            and update_data["authorization_code"]
            != travel_authorization.authorization_code
        ):
            existing = (
                self.travel_authorization_repository.get_by_code(
                    db,
                    update_data["authorization_code"],
                )
            )
            if existing:
                raise TravelAuthorizationAlreadyExistsError(
                    "authorization_code",
                    update_data["authorization_code"],
                )

        if (
            "authorization_name" in update_data
            and update_data["authorization_name"]
            != travel_authorization.authorization_name
        ):
            existing = (
                self.travel_authorization_repository.get_by_name(
                    db,
                    update_data["authorization_name"],
                )
            )
            if existing:
                raise TravelAuthorizationAlreadyExistsError(
                    "authorization_name",
                    update_data["authorization_name"],
                )

        if "destination_country_id" in update_data:
            country = self.country_repository.get_by_id(
                db,
                update_data["destination_country_id"],
            )
            if not country:
                raise CountryNotFoundError(
                    update_data["destination_country_id"],
                )

        for field, value in update_data.items():
            setattr(
                travel_authorization,
                field,
                value,
            )

        return self.travel_authorization_repository.save(
            db,
            travel_authorization,
        )

    def delete_travel_authorization(
        self,
        db: Session,
        travel_authorization_id: int,
    ) -> None:
        """Delete a travel authorization."""

        travel_authorization = (
            self.travel_authorization_repository.get_by_id(
                db,
                travel_authorization_id,
            )
        )

        if not travel_authorization:
            raise TravelAuthorizationNotFoundError(
                travel_authorization_id,
            )

        self.travel_authorization_repository.delete(
            db,
            travel_authorization,
        )