from sqlalchemy.orm import Session

from src.exceptions.reference.region import (
    RegionAlreadyExistsError,
    RegionNotFoundError,
)
from src.models.reference.region import Region
from src.repositories.reference.region_repository import RegionRepository
from src.schemas.reference.region import (
    RegionCreate,
    RegionUpdate,
)
from src.services.base_crud_service import BaseCrudService

class RegionService:
    """Service layer for Region."""

    def __init__(
        self,
        region_repository: RegionRepository,
    ):
        self.region_repository = region_repository
        self.base_crud = BaseCrudService(region_repository)

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

        return self.base_crud.create(
            db=db,
            model=Region,
            data=region_data,
        )

    def get_region(
        self,
        db: Session,
        region_id: int,
    ) -> Region:
        """Get a region by ID."""

        region = self.base_crud.get_by_id(
            db=db,
            obj_id=region_id,
        )

        if not region:
            raise RegionNotFoundError(region_id)

        return region

    def get_all_regions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Region]:
        """Get all regions."""


        return self.base_crud.get_all(db, skip, limit)

    def update_region(
        self,
        db: Session,
        region_id: int,
        region_data: RegionUpdate,
    ) -> Region:
        """Update a region."""

        region = self.base_crud.get_by_id(
            db=db,
            obj_id=region_id,
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

        return self.base_crud.update(
            db=db,
            obj=region,
            data=region_data,
        )

    def delete_region(
        self,
        db: Session,
        region_id: int,
    ) -> None:
        """Delete a region."""

        region = self.base_crud.get_by_id(
            db=db,
            obj_id=region_id,
        )

        if not region:
            raise RegionNotFoundError(region_id)

        self.base_crud.delete(
            db=db,
            obj=region,
        )