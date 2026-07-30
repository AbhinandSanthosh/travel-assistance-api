from sqlalchemy.orm import Session

from src.exceptions.reference.visa_type import (
    VisaTypeAlreadyExistsError,
    VisaTypeNotFoundError,
)
from src.models.reference.visa_type import VisaType
from src.repositories.reference.visa_type_repository import (
    VisaTypeRepository,
)
from src.schemas.reference.visa_type import (
    VisaTypeCreate,
    VisaTypeUpdate,
)
from src.services.base_crud_service import BaseCrudService


class VisaTypeService:
    """Service layer for VisaType."""

    def __init__(
        self,
        visa_type_repository: VisaTypeRepository,
    ):
        self.visa_type_repository = visa_type_repository
        self.base_crud = BaseCrudService(
            visa_type_repository,
        )

    def create_visa_type(
        self,
        db: Session,
        visa_type_data: VisaTypeCreate,
    ) -> VisaType:
        """Create a new visa type."""

        existing_code = self.visa_type_repository.get_by_code(
            db,
            visa_type_data.visa_code,
        )
        if existing_code:
            raise VisaTypeAlreadyExistsError(
                "visa_code",
                visa_type_data.visa_code,
            )

        existing_name = self.visa_type_repository.get_by_name(
            db,
            visa_type_data.visa_name,
        )
        if existing_name:
            raise VisaTypeAlreadyExistsError(
                "visa_name",
                visa_type_data.visa_name,
            )

        return self.base_crud.create(
            db=db,
            model=VisaType,
            data=visa_type_data,
        )

    def get_visa_type(
        self,
        db: Session,
        visa_type_id: int,
    ) -> VisaType:
        """Get a visa type by ID."""

        visa_type = self.base_crud.get_by_id(
            db=db,
            obj_id=visa_type_id,
        )

        if not visa_type:
            raise VisaTypeNotFoundError(
                visa_type_id,
            )

        return visa_type

    def get_all_visa_types(
        self,
        db: Session,
    ) -> list[VisaType]:
        """Get all visa types."""

        return self.base_crud.get_all(db)

    def update_visa_type(
        self,
        db: Session,
        visa_type_id: int,
        visa_type_data: VisaTypeUpdate,
    ) -> VisaType:
        """Update a visa type."""

        visa_type = self.base_crud.get_by_id(
            db=db,
            obj_id=visa_type_id,
        )

        if not visa_type:
            raise VisaTypeNotFoundError(
                visa_type_id,
            )

        update_data = visa_type_data.model_dump(
            exclude_unset=True,
        )

        if (
            "visa_code" in update_data
            and update_data["visa_code"]
            != visa_type.visa_code
        ):
            existing = self.visa_type_repository.get_by_code(
                db,
                update_data["visa_code"],
            )
            if existing:
                raise VisaTypeAlreadyExistsError(
                    "visa_code",
                    update_data["visa_code"],
                )

        if (
            "visa_name" in update_data
            and update_data["visa_name"]
            != visa_type.visa_name
        ):
            existing = self.visa_type_repository.get_by_name(
                db,
                update_data["visa_name"],
            )
            if existing:
                raise VisaTypeAlreadyExistsError(
                    "visa_name",
                    update_data["visa_name"],
                )

        return self.base_crud.update(
            db=db,
            obj=visa_type,
            data=visa_type_data,
        )

    def delete_visa_type(
        self,
        db: Session,
        visa_type_id: int,
    ) -> None:
        """Delete a visa type."""

        visa_type = self.base_crud.get_by_id(
            db=db,
            obj_id=visa_type_id,
        )

        if not visa_type:
            raise VisaTypeNotFoundError(
                visa_type_id,
            )

        self.base_crud.delete(
            db=db,
            obj=visa_type,
        )