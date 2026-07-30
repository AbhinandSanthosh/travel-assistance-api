from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.administration.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User-specific database operations."""

    def __init__(self) -> None:
        super().__init__(User)

    def get_by_username(
        self,
        db: Session,
        username: str,
    ) -> User | None:
        return db.scalar(
            select(User).where(
                User.username == username
            )
        )

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        return db.scalar(
            select(User).where(
                User.email == email
            )
        )