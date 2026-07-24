from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_region_service
from src.db.session import get_db
from src.schemas.reference.region import (
    RegionCreate,
    RegionResponse,
    RegionUpdate,
)
from src.services.reference.region_service import RegionService

router = APIRouter(
    prefix="/regions",
    tags=["Regions"],
)


@router.post(
    "",
    response_model=RegionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_region(
    region_data: RegionCreate,
    db: Session = Depends(get_db),
    service: RegionService = Depends(get_region_service),
):
    """Create a new region."""
    return service.create_region(db, region_data)


@router.get(
    "",
    response_model=list[RegionResponse],
)
def get_all_regions(
    db: Session = Depends(get_db),
    service: RegionService = Depends(get_region_service),
):
    """Get all regions."""
    return service.get_all_regions(db)


@router.get(
    "/{region_id}",
    response_model=RegionResponse,
)
def get_region(
    region_id: int,
    db: Session = Depends(get_db),
    service: RegionService = Depends(get_region_service),
):
    """Get a region by ID."""
    return service.get_region(db, region_id)


@router.put(
    "/{region_id}",
    response_model=RegionResponse,
)
def update_region(
    region_id: int,
    region_data: RegionUpdate,
    db: Session = Depends(get_db),
    service: RegionService = Depends(get_region_service),
):
    """Update a region."""
    return service.update_region(
        db,
        region_id,
        region_data,
    )


@router.delete(
    "/{region_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_region(
    region_id: int,
    db: Session = Depends(get_db),
    service: RegionService = Depends(get_region_service),
):
    """Delete a region."""
    service.delete_region(db, region_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)