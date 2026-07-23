from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.reference.passport_type import PassportType
from src.repositories.base_repository import BaseRepository


class PassportTypeRepository(BaseRepository[PassportType]):
    """Repository for PassportType model."""

    def __init__(self):
        super().__init__(PassportType)

    def get_by_code(
        self,
        db: Session,
        passport_code: str,
    ) -> PassportType | None:
        """Get a passport type by its code."""
        stmt = select(PassportType).where(
            PassportType.passport_code == passport_code,
        )
        return db.scalar(stmt)

    def get_by_name(
        self,
        db: Session,
        passport_name: str,
    ) -> PassportType | None:
        """Get a passport type by its name."""
        stmt = select(PassportType).where(
            PassportType.passport_name == passport_name,
        )
        return db.scalar(stmt)