from sqlalchemy.orm import Session

from src.core.security import hash_password

from src.exceptions.administration.role import (
    RoleNotFoundError,
)
from src.exceptions.administration.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
)

from src.repositories.administration.role import (
    RoleRepository,
)
from src.repositories.administration.user import (
    UserRepository,
)

from src.schemas.administration.user import (
    UserCreate,
    UserUpdate,
)

from src.services.base_crud_service import BaseCrudService


class UserService:
    """Service for User business logic."""

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ) -> None:
        self.user_repository = user_repository
        self.role_repository = role_repository

        self.base_crud = BaseCrudService(
            user_repository,
        )

    def create_user(
        self,
        db: Session,
        user_data: UserCreate,
    ):
        """Create a new user."""

        if self.user_repository.get_by_username(
            db,
            user_data.username,
        ):
            raise UserAlreadyExistsError(
                "username",
                user_data.username,
            )

        if self.user_repository.get_by_email(
            db,
            user_data.email,
        ):
            raise UserAlreadyExistsError(
                "email",
                user_data.email,
            )

        role = self.role_repository.get_by_id(
            db,
            user_data.role_id,
        )

        if role is None:
            raise RoleNotFoundError(
                user_data.role_id,
            )

        payload = user_data.model_dump()

        payload["password_hash"] = hash_password(
            payload.pop("password")
        )

        return self.base_crud.create(
            db,
            payload,
        )

    def get_all_users(
        self,
        db: Session,
    ):
        """Retrieve all users."""
        return self.base_crud.get_all(db)

    def get_user(
        self,
        db: Session,
        user_id: int,
    ):
        """Retrieve a user by ID."""

        user = self.base_crud.get_by_id(
            db,
            user_id,
        )

        if user is None:
            raise UserNotFoundError(
                user_id,
            )

        return user

    def update_user(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate,
    ):
        """Update an existing user."""

        user = self.get_user(
            db,
            user_id,
        )

        update_data = user_data.model_dump(
            exclude_unset=True,
        )

        if (
            "username" in update_data
            and update_data["username"] != user.username
        ):
            existing = self.user_repository.get_by_username(
                db,
                update_data["username"],
            )

            if existing:
                raise UserAlreadyExistsError(
                    "username",
                    update_data["username"],
                )

        if (
            "email" in update_data
            and update_data["email"] != user.email
        ):
            existing = self.user_repository.get_by_email(
                db,
                update_data["email"],
            )

            if existing:
                raise UserAlreadyExistsError(
                    "email",
                    update_data["email"],
                )

        if "role_id" in update_data:
            role = self.role_repository.get_by_id(
                db,
                update_data["role_id"],
            )

            if role is None:
                raise RoleNotFoundError(
                    update_data["role_id"],
                )

        if "password" in update_data:
            update_data["password_hash"] = hash_password(
                update_data.pop("password")
            )

        return self.base_crud.update(
            db,
            user,
            update_data,
        )

    def delete_user(
        self,
        db: Session,
        user_id: int,
    ):
        """Delete a user."""

        user = self.get_user(
            db,
            user_id,
        )

        self.base_crud.delete(
            db,
            user,
        )