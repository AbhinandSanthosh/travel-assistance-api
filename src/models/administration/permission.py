from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base_model import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role_permission import RolePermission


class Permission(BaseModel):
    __tablename__ = "permissions"

    permission_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    permission_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="permission",
    )