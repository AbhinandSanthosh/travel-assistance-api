from sqlalchemy.orm import Session

from src.exceptions.administration.role_permission import (
    RolePermissionAlreadyExistsError,
    RolePermissionNotFoundError,
)
from src.exceptions.administration.role import (
    RoleNotFoundError,
)
from src.exceptions.administration.permission import (
    PermissionNotFoundError,
)

from src.models.administration.role_permission import (
    RolePermission,
)

from src.repositories.administration.role_permission import (
    RolePermissionRepository,
)
from src.repositories.administration.role import (
    RoleRepository,
)
from src.repositories.administration.permission import (
    PermissionRepository,
)

from src.schemas.administration.role_permission import (
    RolePermissionCreate,
    RolePermissionUpdate,
)

from src.services.base_crud_service import BaseCrudService


class RolePermissionService:
    """Service layer for RolePermission business logic."""

    def __init__(
        self,
        role_permission_repository: RolePermissionRepository,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
    ):
        self.role_permission_repository = (
            role_permission_repository
        )
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.base_crud = BaseCrudService(
            role_permission_repository
        )

    def create_role_permission(
        self,
        db: Session,
        role_permission_data: RolePermissionCreate,
    ) -> RolePermission:
        """Create a new role-permission mapping."""

        role = self.role_repository.get_by_id(
            db,
            role_permission_data.role_id,
        )

        if not role:
            raise RoleNotFoundError(
                role_permission_data.role_id,
            )

        permission = self.permission_repository.get_by_id(
            db,
            role_permission_data.permission_id,
        )

        if not permission:
            raise PermissionNotFoundError(
                role_permission_data.permission_id,
            )

        existing = (
            self.role_permission_repository.get_by_role_and_permission(
                db,
                role_permission_data.role_id,
                role_permission_data.permission_id,
            )
        )

        if existing is not None:
            raise RolePermissionAlreadyExistsError(
                role_permission_data.role_id,
                role_permission_data.permission_id,
            )

        return self.base_crud.create(
            db=db,
            model=RolePermission,
            data=role_permission_data,
        )

    def get_role_permission(
        self,
        db: Session,
        role_permission_id: int,
    ) -> RolePermission:
        """Retrieve a role-permission mapping by ID."""

        role_permission = self.base_crud.get_by_id(
            db=db,
            obj_id=role_permission_id,
        )

        if role_permission is None:
            raise RolePermissionNotFoundError(
                role_permission_id,
            )

        return role_permission

    def get_all_role_permissions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RolePermission]:
        """Retrieve all role-permission mappings."""

        return self.base_crud.get_all(db, skip, limit)

    def update_role_permission(
        self,
        db: Session,
        role_permission_id: int,
        role_permission_data: RolePermissionUpdate,
    ) -> RolePermission:
        """Update an existing role-permission mapping."""

        role_permission = self.get_role_permission(
            db=db,
            role_permission_id=role_permission_id,
        )

        update_data = role_permission_data.model_dump(
            exclude_unset=True,
        )

        new_role_id = update_data.get(
            "role_id",
            role_permission.role_id,
        )

        new_permission_id = update_data.get(
            "permission_id",
            role_permission.permission_id,
        )

        role = self.role_repository.get_by_id(
            db,
            new_role_id,
        )

        if not role:
            raise RoleNotFoundError(new_role_id)

        permission = self.permission_repository.get_by_id(
            db,
            new_permission_id,
        )

        if not permission:
            raise PermissionNotFoundError(
                new_permission_id,
            )

        existing = (
            self.role_permission_repository.get_by_role_and_permission(
                db,
                new_role_id,
                new_permission_id,
            )
        )

        if (
            existing is not None
            and existing.id != role_permission.id
        ):
            raise RolePermissionAlreadyExistsError(
                new_role_id,
                new_permission_id,
            )

        return self.base_crud.update(
            db=db,
            obj=role_permission,
            data=role_permission_data,
        )

    def delete_role_permission(
        self,
        db: Session,
        role_permission_id: int,
    ) -> None:
        """Delete a role-permission mapping."""

        role_permission = self.get_role_permission(
            db=db,
            role_permission_id=role_permission_id,
        )

        self.base_crud.delete(
            db=db,
            obj=role_permission,
        )