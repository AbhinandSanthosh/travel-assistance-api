from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .role_permission import RolePermission


class Role(BaseModel):
    __tablename__ = "roles"

    role_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
    )