from sqlalchemy.orm import Session

from src.exceptions.reference.passport_type import (
    PassportTypeAlreadyExistsError,
    PassportTypeNotFoundError,
)
from src.models.reference.passport_type import PassportType
from src.repositories.reference.passport_type_repository import (
    PassportTypeRepository,
)
from src.schemas.reference.passport_type import (
    PassportTypeCreate,
    PassportTypeUpdate,
)
from src.services.base_crud_service import BaseCrudService


class PassportTypeService:
    """Service layer for PassportType."""

    def __init__(
        self,
        passport_type_repository: PassportTypeRepository,
    ):
        self.passport_type_repository = passport_type_repository
        self.base_crud = BaseCrudService(
            passport_type_repository,
        )

    def create_passport_type(
        self,
        db: Session,
        passport_type_data: PassportTypeCreate,
    ) -> PassportType:
        """Create a new passport type."""

        existing_code = self.passport_type_repository.get_by_code(
            db,
            passport_type_data.passport_code,
        )
        if existing_code:
            raise PassportTypeAlreadyExistsError(
                "passport_code",
                passport_type_data.passport_code,
            )

        existing_name = self.passport_type_repository.get_by_name(
            db,
            passport_type_data.passport_name,
        )
        if existing_name:
            raise PassportTypeAlreadyExistsError(
                "passport_name",
                passport_type_data.passport_name,
            )

        return self.base_crud.create(
            db=db,
            model=PassportType,
            data=passport_type_data,
        )

    def get_passport_type(
        self,
        db: Session,
        passport_type_id: int,
    ) -> PassportType:
        """Get a passport type by ID."""

        passport_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passport_type_id,
        )

        if not passport_type:
            raise PassportTypeNotFoundError(
                passport_type_id,
            )

        return passport_type

    def get_all_passport_types(
        self,
        db: Session,
    ) -> list[PassportType]:
        """Get all passport types."""

        return self.base_crud.get_all(db)

    def update_passport_type(
        self,
        db: Session,
        passport_type_id: int,
        passport_type_data: PassportTypeUpdate,
    ) -> PassportType:
        """Update a passport type."""

        passport_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passport_type_id,
        )

        if not passport_type:
            raise PassportTypeNotFoundError(
                passport_type_id,
            )

        update_data = passport_type_data.model_dump(
            exclude_unset=True,
        )

        if (
            "passport_code" in update_data
            and update_data["passport_code"]
            != passport_type.passport_code
        ):
            existing = self.passport_type_repository.get_by_code(
                db,
                update_data["passport_code"],
            )
            if existing:
                raise PassportTypeAlreadyExistsError(
                    "passport_code",
                    update_data["passport_code"],
                )

        if (
            "passport_name" in update_data
            and update_data["passport_name"]
            != passport_type.passport_name
        ):
            existing = self.passport_type_repository.get_by_name(
                db,
                update_data["passport_name"],
            )
            if existing:
                raise PassportTypeAlreadyExistsError(
                    "passport_name",
                    update_data["passport_name"],
                )

        return self.base_crud.update(
            db=db,
            obj=passport_type,
            data=passport_type_data,
        )

    def delete_passport_type(
        self,
        db: Session,
        passport_type_id: int,
    ) -> None:
        """Delete a passport type."""

        passport_type = self.base_crud.get_by_id(
            db=db,
            obj_id=passport_type_id,
        )

        if not passport_type:
            raise PassportTypeNotFoundError(
                passport_type_id,
            )

        self.base_crud.delete(
            db=db,
            obj=passport_type,
        )