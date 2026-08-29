from sqlalchemy.orm import Session

from src.exceptions.administration.permission import (
    PermissionAlreadyExistsError,
    PermissionNotFoundError,
)

from src.models.administration.permission import Permission

from src.repositories.administration.permission import (
    PermissionRepository,
)

from src.schemas.administration.permission import (
    PermissionCreate,
    PermissionUpdate,
)

from src.services.base_crud_service import BaseCrudService


class PermissionService:
    """Service layer for Permission business logic."""

    def __init__(
        self,
        permission_repository: PermissionRepository,
    ):
        self.permission_repository = permission_repository
        self.base_crud = BaseCrudService(permission_repository)

    def create_permission(
        self,
        db: Session,
        permission_data: PermissionCreate,
    ) -> Permission:
        """Create a new permission."""

        existing = self.permission_repository.get_by_permission_code(
            db,
            permission_data.permission_code,
        )

        if existing is not None:
            raise PermissionAlreadyExistsError(
                field="permission_code",
                value=permission_data.permission_code,
            )

        return self.base_crud.create(
            db=db,
            model=Permission,
            data=permission_data,
        )

    def get_permission(
        self,
        db: Session,
        permission_id: int,
    ) -> Permission:
        """Retrieve a permission by ID."""

        permission = self.base_crud.get_by_id(
            db=db,
            obj_id=permission_id,
        )

        if permission is None:
            raise PermissionNotFoundError(permission_id)

        return permission

    def get_all_permissions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Permission]:
        """Retrieve all permissions."""

        return self.base_crud.get_all(db, skip, limit)

    def update_permission(
        self,
        db: Session,
        permission_id: int,
        permission_data: PermissionUpdate,
    ) -> Permission:
        """Update an existing permission."""

        permission = self.get_permission(
            db=db,
            permission_id=permission_id,
        )

        update_data = permission_data.model_dump(
            exclude_unset=True,
        )

        if (
            "permission_code" in update_data
            and update_data["permission_code"] != permission.permission_code
        ):
            existing = self.permission_repository.get_by_permission_code(
                db,
                update_data["permission_code"],
            )

            if existing is not None:
                raise PermissionAlreadyExistsError(
                    field="permission_code",
                    value=update_data["permission_code"],
                )

        return self.base_crud.update(
            db=db,
            obj=permission,
            data=permission_data,
        )

    def delete_permission(
        self,
        db: Session,
        permission_id: int,
    ) -> None:
        """Delete a permission."""

        permission = self.get_permission(
            db=db,
            permission_id=permission_id,
        )

        self.base_crud.delete(
            db=db,
            obj=permission,
        )