from fastapi import APIRouter, Depends, Response, status
from src.api.dependencies.auth import require_permission
from sqlalchemy.orm import Session

from src.api.dependencies.administration import get_role_service
from src.db.session import get_db

from src.schemas.administration.role import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)

from src.services.administration.role import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post(
    "",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Create a new role."""
    return service.create_role(db, role_data)


@router.get(
    "",
    response_model=list[RoleResponse],
)
def get_all_roles(
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_role_service),
) -> list[RoleResponse]:
    """Retrieve all roles."""
    return service.get_all_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Retrieve a role by ID."""
    return service.get_role(db, role_id)


@router.put(
    "/{role_id}",
    dependencies=[Depends(require_permission("administration.write"))],
    response_model=RoleResponse,
)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_role_service),
) -> RoleResponse:
    """Update an existing role."""
    return service.update_role(
        db=db,
        role_id=role_id,
        role_data=role_data,
    )


@router.delete(
    "/{role_id}",
    dependencies=[Depends(require_permission("administration.write"))],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_role_service),
) -> Response:
    """Delete a role."""
    service.delete_role(db, role_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )