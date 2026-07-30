from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.api.dependencies.administration import (
    get_role_permission_service,
)
from src.db.session import get_db

from src.schemas.administration.role_permission import (
    RolePermissionCreate,
    RolePermissionResponse,
    RolePermissionUpdate,
)

from src.services.administration.role_permission import (
    RolePermissionService,
)

router = APIRouter(
    prefix="/role-permissions",
    tags=["Role Permissions"],
)


@router.post(
    "",
    response_model=RolePermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role_permission(
    role_permission_data: RolePermissionCreate,
    db: Session = Depends(get_db),
    service: RolePermissionService = Depends(
        get_role_permission_service,
    ),
) -> RolePermissionResponse:
    """Create a new role-permission mapping."""
    return service.create_role_permission(
        db,
        role_permission_data,
    )


@router.get(
    "",
    response_model=list[RolePermissionResponse],
)
def get_all_role_permissions(
    db: Session = Depends(get_db),
    service: RolePermissionService = Depends(
        get_role_permission_service,
    ),
) -> list[RolePermissionResponse]:
    """Retrieve all role-permission mappings."""
    return service.get_all_role_permissions(db)


@router.get(
    "/{role_permission_id}",
    response_model=RolePermissionResponse,
)
def get_role_permission(
    role_permission_id: int,
    db: Session = Depends(get_db),
    service: RolePermissionService = Depends(
        get_role_permission_service,
    ),
) -> RolePermissionResponse:
    """Retrieve a role-permission mapping by ID."""
    return service.get_role_permission(
        db,
        role_permission_id,
    )


@router.put(
    "/{role_permission_id}",
    response_model=RolePermissionResponse,
)
def update_role_permission(
    role_permission_id: int,
    role_permission_data: RolePermissionUpdate,
    db: Session = Depends(get_db),
    service: RolePermissionService = Depends(
        get_role_permission_service,
    ),
) -> RolePermissionResponse:
    """Update an existing role-permission mapping."""
    return service.update_role_permission(
        db=db,
        role_permission_id=role_permission_id,
        role_permission_data=role_permission_data,
    )


@router.delete(
    "/{role_permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role_permission(
    role_permission_id: int,
    db: Session = Depends(get_db),
    service: RolePermissionService = Depends(
        get_role_permission_service,
    ),
) -> Response:
    """Delete a role-permission mapping."""
    service.delete_role_permission(
        db,
        role_permission_id,
    )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )