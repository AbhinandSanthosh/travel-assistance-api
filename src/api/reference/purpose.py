from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.reference import get_purpose_service
from src.db.session import get_db
from src.schemas.reference.purpose import (
    PurposeCreate,
    PurposeResponse,
    PurposeUpdate,
)
from src.services.reference.purpose_service import (
    PurposeService,
)

router = APIRouter(
    prefix="/purposes",
    tags=["Purposes"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=PurposeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_purpose(
    purpose_data: PurposeCreate,
    db: Session = Depends(get_db),
    service: PurposeService = Depends(
        get_purpose_service,
    ),
):
    """Create a new purpose."""
    return service.create_purpose(
        db,
        purpose_data,
    )


@router.get(
    "",
    response_model=list[PurposeResponse],
)
def get_all_purposes(
    db: Session = Depends(get_db),
    service: PurposeService = Depends(
        get_purpose_service,
    ),
):
    """Retrieve all purposes."""
    return service.get_all_purposes(db)


@router.get(
    "/{purpose_id}",
    response_model=PurposeResponse,
)
def get_purpose(
    purpose_id: int,
    db: Session = Depends(get_db),
    service: PurposeService = Depends(
        get_purpose_service,
    ),
):
    """Retrieve a purpose by ID."""
    return service.get_purpose(
        db,
        purpose_id,
    )


@router.put(
    "/{purpose_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    response_model=PurposeResponse,
)
def update_purpose(
    purpose_id: int,
    purpose_data: PurposeUpdate,
    db: Session = Depends(get_db),
    service: PurposeService = Depends(
        get_purpose_service,
    ),
):
    """Update a purpose."""
    return service.update_purpose(
        db,
        purpose_id,
        purpose_data,
    )


@router.delete(
    "/{purpose_id}",
    dependencies=[Depends(require_permission("reference.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_purpose(
    purpose_id: int,
    db: Session = Depends(get_db),
    service: PurposeService = Depends(
        get_purpose_service,
    ),
):
    """Delete a purpose."""
    service.delete_purpose(
        db,
        purpose_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )