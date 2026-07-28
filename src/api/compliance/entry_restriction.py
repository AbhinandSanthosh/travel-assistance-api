from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_entry_restriction_service,
)
from src.db.session import get_db
from src.schemas.compliance.entry_restriction import (
    EntryRestrictionCreate,
    EntryRestrictionResponse,
    EntryRestrictionUpdate,
)
from src.services.compliance.entry_restriction import (
    EntryRestrictionService,
)

router = APIRouter(
    prefix="/entry-restrictions",
    tags=["Entry Restrictions"],
)


@router.post(
    "",
    response_model=EntryRestrictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_entry_restriction(
    entry_restriction_data: EntryRestrictionCreate,
    db: Session = Depends(get_db),
    service: EntryRestrictionService = Depends(
        get_entry_restriction_service,
    ),
) -> EntryRestrictionResponse:
    """Create a new entry restriction."""
    return service.create_entry_restriction(
        db,
        entry_restriction_data,
    )


@router.get(
    "",
    response_model=list[EntryRestrictionResponse],
)
def get_all_entry_restrictions(
    db: Session = Depends(get_db),
    service: EntryRestrictionService = Depends(
        get_entry_restriction_service,
    ),
) -> list[EntryRestrictionResponse]:
    """Retrieve all entry restrictions."""
    return service.get_all_entry_restrictions(
        db,
    )


@router.get(
    "/{entry_restriction_id}",
    response_model=EntryRestrictionResponse,
)
def get_entry_restriction(
    entry_restriction_id: int,
    db: Session = Depends(get_db),
    service: EntryRestrictionService = Depends(
        get_entry_restriction_service,
    ),
) -> EntryRestrictionResponse:
    """Retrieve an entry restriction by ID."""
    return service.get_entry_restriction(
        db,
        entry_restriction_id,
    )


@router.put(
    "/{entry_restriction_id}",
    response_model=EntryRestrictionResponse,
)
def update_entry_restriction(
    entry_restriction_id: int,
    entry_restriction_data: EntryRestrictionUpdate,
    db: Session = Depends(get_db),
    service: EntryRestrictionService = Depends(
        get_entry_restriction_service,
    ),
) -> EntryRestrictionResponse:
    """Update an existing entry restriction."""
    return service.update_entry_restriction(
        db=db,
        entry_restriction_id=entry_restriction_id,
        entry_restriction_data=entry_restriction_data,
    )


@router.delete(
    "/{entry_restriction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entry_restriction(
    entry_restriction_id: int,
    db: Session = Depends(get_db),
    service: EntryRestrictionService = Depends(
        get_entry_restriction_service,
    ),
) -> Response:
    """Delete an entry restriction."""
    service.delete_entry_restriction(
        db,
        entry_restriction_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )