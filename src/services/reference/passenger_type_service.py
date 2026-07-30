from sqlalchemy.orm import Session

from src.exceptions.reference.passenger_type import (
    PassengerTypeAlreadyExistsError,
    PassengerTypeNotFoundError,
)
from src.models.reference.passenger_type import PassengerType
from src.repositories.reference.passenger_type_repository import (
    PassengerTypeRepository,
)
from src.schemas.reference.passenger_type import (
    PassengerTypeCreate,
    PassengerTypeUpdate,
)
from src.services.base_crud_service import BaseCrudService


class PassengerTypeService:
    """Service layer for PassengerType."""

    def __init__(
        self,
        passenger_type_repository: PassengerTypeRepository,
    ):
        self.passenger_type_repository = passenger_type_repository
        self.base_crud = BaseCrudService(
            passenger_type_repository,
        )

    def create_passenger_type(
        self,
        db: Session,
        passenger_type_data: PassengerTypeCreate,
    ) -> PassengerType:
        """Create a new passenger type."""

        existing_code = (
            self.passenger_type_repository.get_by_code(
                db,
                passenger_type_data.passenger_type_code,
            )
        )
        if existing_code:
            raise PassengerTypeAlreadyExistsError(
                "passenger_type_code",
                passenger_type_data.passenger_type_code,
            )

        existing_name = (
            self.passenger_type_repository.get_by_name(
                db,
                passenger_type_data.passenger_type_name,
            )
        )
        if existing_name:
            raise PassengerTypeAlreadyExistsError(
                "passenger_type_name",
                passenger_type_data.passenger_type_name,
            )

        return self.base_crud.create(
            db=db,
            model=PassengerType,
            data=passenger_type_data,
        )

    def get_passenger_type(
        self,
        db: Session,
        passenger_type_id: int,
    ) -> PassengerType:
        """Get a passenger type by ID."""

        passenger_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passenger_type_id,
        )

        if not passenger_type:
            raise PassengerTypeNotFoundError(
                passenger_type_id,
            )

        return passenger_type

    def get_all_passenger_types(
        self,
        db: Session,
    ) -> list[PassengerType]:
        """Get all passenger types."""

        return self.base_crud.get_all(db)

    def update_passenger_type(
        self,
        db: Session,
        passenger_type_id: int,
        passenger_type_data: PassengerTypeUpdate,
    ) -> PassengerType:
        """Update a passenger type."""

        passenger_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passenger_type_id,
        )

        if not passenger_type:
            raise PassengerTypeNotFoundError(
                passenger_type_id,
            )

        update_data = passenger_type_data.model_dump(
            exclude_unset=True,
        )

        if (
            "passenger_type_code" in update_data
            and update_data["passenger_type_code"]
            != passenger_type.passenger_type_code
        ):
            existing = (
                self.passenger_type_repository.get_by_code(
                    db,
                    update_data["passenger_type_code"],
                )
            )
            if existing:
                raise PassengerTypeAlreadyExistsError(
                    "passenger_type_code",
                    update_data["passenger_type_code"],
                )

        if (
            "passenger_type_name" in update_data
            and update_data["passenger_type_name"]
            != passenger_type.passenger_type_name
        ):
            existing = (
                self.passenger_type_repository.get_by_name(
                    db,
                    update_data["passenger_type_name"],
                )
            )
            if existing:
                raise PassengerTypeAlreadyExistsError(
                    "passenger_type_name",
                    update_data["passenger_type_name"],
                )

        return self.base_crud.update(
            db=db,
            obj=passenger_type,
            data=passenger_type_data,
        )

    def delete_passenger_type(
        self,
        db: Session,
        passenger_type_id: int,
    ) -> None:
        """Delete a passenger type."""

        passenger_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passenger_type_id,
        )

        if not passenger_type:
            raise PassengerTypeNotFoundError(
                passenger_type_id,
            )

        self.base_crud.delete(
            db=db,
            obj=passenger_type,
        )