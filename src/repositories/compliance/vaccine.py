from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.vaccine import Vaccine
from src.repositories.base_repository import BaseRepository


class VaccineRepository(
    BaseRepository[Vaccine],
):
    """Repository for Vaccine-specific database operations."""

    def __init__(self) -> None:
        super().__init__(Vaccine)

    def get_by_vaccine_name(
        self,
        db: Session,
        vaccine_name: str,
    ) -> Vaccine | None:
        return db.scalar(
            select(Vaccine).where(
                Vaccine.vaccine_name == vaccine_name
            )
        )