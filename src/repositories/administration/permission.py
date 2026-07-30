from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.permission import Permission
from src.repositories.base_repository import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """Repository for Permission-specific database operations."""

    def __init__(self) -> None:
        super().__init__(Permission)

    def get_by_permission_code(
        self,
        db: Session,
        permission_code: str,
    ) -> Permission | None:
        return db.scalar(
            select(Permission).where(
                Permission.permission_code == permission_code
            )
        )