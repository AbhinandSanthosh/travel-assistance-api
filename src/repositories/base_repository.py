from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing common CRUD operations."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_by_id(self, db: Session, obj_id: int) -> ModelType | None:
        return db.get(self.model, obj_id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.scalars(
            select(self.model).offset(skip).limit(limit)
        ).all()

    def delete(self, db: Session, obj: ModelType) -> None:
        db.delete(obj)
        db.commit()

    def save(self, db: Session, obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(obj)
        return obj