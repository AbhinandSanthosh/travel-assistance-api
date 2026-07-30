from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role
    from .permission import Permission


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="role_permissions",
    )

    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="role_permissions",
    )