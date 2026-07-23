from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.reference.visa_type import VisaType
from src.repositories.base_repository import BaseRepository


class VisaTypeRepository(BaseRepository[VisaType]):
    """Repository for VisaType model."""

    def __init__(self):
        super().__init__(VisaType)

    def get_by_code(
        self,
        db: Session,
        visa_code: str,
    ) -> VisaType | None:
        """Get a visa type by its code."""
        stmt = select(VisaType).where(
            VisaType.visa_code == visa_code,
        )
        return db.scalar(stmt)

    def get_by_name(
        self,
        db: Session,
        visa_name: str,
    ) -> VisaType | None:
        """Get a visa type by its name."""
        stmt = select(VisaType).where(
            VisaType.visa_name == visa_name,
        )
        return db.scalar(stmt)