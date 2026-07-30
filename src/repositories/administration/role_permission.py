from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.role_permission import (
    RolePermission,
)
from src.repositories.base_repository import BaseRepository


class RolePermissionRepository(
    BaseRepository[RolePermission]
):
    """Repository for RolePermission-specific database operations."""

    def __init__(self) -> None:
        super().__init__(RolePermission)

    def get_by_role_and_permission(
        self,
        db: Session,
        role_id: int,
        permission_id: int,
    ) -> RolePermission | None:
        return db.scalar(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )