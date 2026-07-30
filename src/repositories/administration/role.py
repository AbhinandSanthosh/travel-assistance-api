from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.role import Role
from src.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for Role-specific database operations."""

    def __init__(self) -> None:
        super().__init__(Role)

    def get_by_role_name(
        self,
        db: Session,
        role_name: str,
    ) -> Role | None:
        return db.scalar(
            select(Role).where(
                Role.role_name == role_name
            )
        )