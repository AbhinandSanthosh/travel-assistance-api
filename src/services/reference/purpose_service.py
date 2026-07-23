from sqlalchemy.orm import Session

from src.exceptions.purpose import (
    PurposeAlreadyExistsError,
    PurposeNotFoundError,
)
from src.models.reference.purpose import Purpose
from src.repositories.reference.purpose_repository import (
    PurposeRepository,
)
from src.schemas.reference.purpose import (
    PurposeCreate,
    PurposeUpdate,
)


class PurposeService:
    """Service layer for Purpose."""

    def __init__(
        self,
        purpose_repository: PurposeRepository,
    ):
        self.purpose_repository = purpose_repository

    def create_purpose(
        self,
        db: Session,
        purpose_data: PurposeCreate,
    ) -> Purpose:
        """Create a new purpose."""

        existing_code = self.purpose_repository.get_by_code(
            db,
            purpose_data.purpose_code,
        )
        if existing_code:
            raise PurposeAlreadyExistsError(
                "purpose_code",
                purpose_data.purpose_code,
            )

        existing_name = self.purpose_repository.get_by_name(
            db,
            purpose_data.purpose_name,
        )
        if existing_name:
            raise PurposeAlreadyExistsError(
                "purpose_name",
                purpose_data.purpose_name,
            )

        purpose = Purpose(
            **purpose_data.model_dump(),
        )

        return self.purpose_repository.create(
            db,
            purpose,
        )

    def get_purpose(
        self,
        db: Session,
        purpose_id: int,
    ) -> Purpose:
        """Get a purpose by ID."""

        purpose = self.purpose_repository.get_by_id(
            db,
            purpose_id,
        )

        if not purpose:
            raise PurposeNotFoundError(
                purpose_id,
            )

        return purpose

    def get_all_purposes(
        self,
        db: Session,
    ) -> list[Purpose]:
        """Get all purposes."""

        return self.purpose_repository.get_all(
            db,
        )

    def update_purpose(
        self,
        db: Session,
        purpose_id: int,
        purpose_data: PurposeUpdate,
    ) -> Purpose:
        """Update a purpose."""

        purpose = self.purpose_repository.get_by_id(
            db,
            purpose_id,
        )

        if not purpose:
            raise PurposeNotFoundError(
                purpose_id,
            )

        update_data = purpose_data.model_dump(
            exclude_unset=True,
        )

        if (
            "purpose_code" in update_data
            and update_data["purpose_code"]
            != purpose.purpose_code
        ):
            existing = self.purpose_repository.get_by_code(
                db,
                update_data["purpose_code"],
            )
            if existing:
                raise PurposeAlreadyExistsError(
                    "purpose_code",
                    update_data["purpose_code"],
                )

        if (
            "purpose_name" in update_data
            and update_data["purpose_name"]
            != purpose.purpose_name
        ):
            existing = self.purpose_repository.get_by_name(
                db,
                update_data["purpose_name"],
            )
            if existing:
                raise PurposeAlreadyExistsError(
                    "purpose_name",
                    update_data["purpose_name"],
                )

        for field, value in update_data.items():
            setattr(
                purpose,
                field,
                value,
            )

        return self.purpose_repository.save(
            db,
            purpose,
        )

    def delete_purpose(
        self,
        db: Session,
        purpose_id: int,
    ) -> None:
        """Delete a purpose."""

        purpose = self.purpose_repository.get_by_id(
            db,
            purpose_id,
        )

        if not purpose:
            raise PurposeNotFoundError(
                purpose_id,
            )

        self.purpose_repository.delete(
            db,
            purpose,
        )