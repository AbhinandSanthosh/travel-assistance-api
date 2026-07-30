from sqlalchemy.orm import Session

from src.exceptions.administration.role import (
    RoleAlreadyExistsError,
    RoleNotFoundError,
)

from src.models.administration.role import Role

from src.repositories.administration.role import RoleRepository

from src.schemas.administration.role import (
    RoleCreate,
    RoleUpdate,
)

from src.services.base_crud_service import BaseCrudService


class RoleService:
    """Service layer for Role business logic."""

    def __init__(
        self,
        role_repository: RoleRepository,
    ):
        self.role_repository = role_repository
        self.base_crud = BaseCrudService(role_repository)

    def create_role(
        self,
        db: Session,
        role_data: RoleCreate,
    ) -> Role:
        """Create a new role."""

        existing = self.role_repository.get_by_role_name(
            db,
            role_data.role_name,
        )

        if existing is not None:
            raise RoleAlreadyExistsError(
                field="role_name",
                value=role_data.role_name,
            )

        return self.base_crud.create(
            db=db,
            model=Role,
            data=role_data,
        )

    def get_role(
        self,
        db: Session,
        role_id: int,
    ) -> Role:
        """Retrieve a role by ID."""

        role = self.base_crud.get_by_id(
            db=db,
            obj_id=role_id,
        )

        if role is None:
            raise RoleNotFoundError(role_id)

        return role

    def get_all_roles(
        self,
        db: Session,
    ) -> list[Role]:
        """Retrieve all roles."""

        return self.base_crud.get_all(db)

    def update_role(
        self,
        db: Session,
        role_id: int,
        role_data: RoleUpdate,
    ) -> Role:
        """Update an existing role."""

        role = self.get_role(
            db=db,
            role_id=role_id,
        )

        update_data = role_data.model_dump(
            exclude_unset=True,
        )

        if (
            "role_name" in update_data
            and update_data["role_name"] != role.role_name
        ):
            existing = self.role_repository.get_by_role_name(
                db,
                update_data["role_name"],
            )

            if existing is not None:
                raise RoleAlreadyExistsError(
                    field="role_name",
                    value=update_data["role_name"],
                )

        return self.base_crud.update(
            db=db,
            obj=role,
            data=role_data,
        )

    def delete_role(
        self,
        db: Session,
        role_id: int,
    ) -> None:
        """Delete a role."""

        role = self.get_role(
            db=db,
            role_id=role_id,
        )

        self.base_crud.delete(
            db=db,
            obj=role,
        )