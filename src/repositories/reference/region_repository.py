from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.reference.region import Region
from src.repositories.base_repository import BaseRepository


class RegionRepository(BaseRepository[Region]):
    """Repository for Region model."""

    def __init__(self):
        super().__init__(Region)

    def get_by_name(
        self,
        db: Session,
        region_name: str,
    ) -> Region | None:
        """Get a region by its name."""
        stmt = select(Region).where(
            Region.region_name == region_name,
        )
        return db.scalar(stmt)