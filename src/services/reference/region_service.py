from sqlalchemy.orm import Session

from src.exceptions.region import (
    RegionAlreadyExistsError,
    RegionNotFoundError,
)
from src.models.reference.region import Region
from src.repositories.reference.region_repository import RegionRepository
from src.schemas.reference.region import (
    RegionCreate,
    RegionUpdate,
)


class RegionService:
    """Service layer for Region."""

    def __init__(
        self,
        region_repository: RegionRepository,
    ):
        self.region_repository = region_repository

    def create_region(
        self,
        db: Session,
        region_data: RegionCreate,
    ) -> Region:
        """Create a new region."""

        existing_region = self.region_repository.get_by_name(
            db,
            region_data.region_name,
        )

        if existing_region:
            raise RegionAlreadyExistsError(
                region_data.region_name,
            )

        region = Region(**region_data.model_dump())

        return self.region_repository.create(
            db,
            region,
        )

    def get_region(
        self,
        db: Session,
        region_id: int,
    ) -> Region:
        """Get a region by ID."""

        region = self.region_repository.get_by_id(
            db,
            region_id,
        )

        if not region:
            raise RegionNotFoundError(region_id)

        return region

    def get_all_regions(
        self,
        db: Session,
    ) -> list[Region]:
        """Get all regions."""

        return self.region_repository.get_all(db)

    def update_region(
        self,
        db: Session,
        region_id: int,
        region_data: RegionUpdate,
    ) -> Region:
        """Update a region."""

        region = self.region_repository.get_by_id(
            db,
            region_id,
        )

        if not region:
            raise RegionNotFoundError(region_id)

        update_data = region_data.model_dump(
            exclude_unset=True,
        )

        if (
            "region_name" in update_data
            and update_data["region_name"] != region.region_name
        ):
            existing_region = self.region_repository.get_by_name(
                db,
                update_data["region_name"],
            )

            if existing_region:
                raise RegionAlreadyExistsError(
                    update_data["region_name"],
                )

        for field, value in update_data.items():
            setattr(region, field, value)

        return self.region_repository.save(
            db,
            region,
        )

    def delete_region(
        self,
        db: Session,
        region_id: int,
    ) -> None:
        """Delete a region."""

        region = self.region_repository.get_by_id(
            db,
            region_id,
        )

        if not region:
            raise RegionNotFoundError(region_id)

        self.region_repository.delete(
            db,
            region,
        )