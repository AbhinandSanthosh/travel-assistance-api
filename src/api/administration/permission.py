from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_permission_service,
)
from src.db.session import get_db

from src.schemas.administration.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)

from src.services.administration.permission import (
    PermissionService,
)

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    service: PermissionService = Depends(
        get_permission_service,
    ),
) -> PermissionResponse:
    """Create a new permission."""
    return service.create_permission(
        db,
        permission_data,
    )


@router.get(
    "",
    response_model=list[PermissionResponse],
)
def get_all_permissions(
    db: Session = Depends(get_db),
    service: PermissionService = Depends(
        get_permission_service,
    ),
) -> list[PermissionResponse]:
    """Retrieve all permissions."""
    return service.get_all_permissions(db)


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    service: PermissionService = Depends(
        get_permission_service,
    ),
) -> PermissionResponse:
    """Retrieve a permission by ID."""
    return service.get_permission(
        db,
        permission_id,
    )


@router.put(
    "/{permission_id}",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=PermissionResponse,
)
def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db),
    service: PermissionService = Depends(
        get_permission_service,
    ),
) -> PermissionResponse:
    """Update an existing permission."""
    return service.update_permission(
        db=db,
        permission_id=permission_id,
        permission_data=permission_data,
    )


@router.delete(
    "/{permission_id}",
    dependencies=[Depends(require_permission("administration.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    service: PermissionService = Depends(
        get_permission_service,
    ),
) -> Response:
    """Delete a permission."""
    service.delete_permission(
        db,
        permission_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )