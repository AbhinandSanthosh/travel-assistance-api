from typing import Any, Type

from sqlalchemy.orm import Session


class BaseCrudService:
    """Generic CRUD service for common database operations."""

    def __init__(self, repository: Any) -> None:
        self.repository = repository

    def create(
        self,
        db: Session,
        model: Type[Any],
        data: Any,
    ) -> Any:
        """Create a new record."""

        obj = model(**data.model_dump())

        return self.repository.create(
            db=db,
            obj=obj,
        )

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ) -> Any:
        """Retrieve a record by its ID."""

        return self.repository.get_by_id(
            db=db,
            obj_id=obj_id,
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Any]:
        """Retrieve records, paginated. Without this cap, a listing
        endpoint on a table that grows without bound (e.g. audit_logs,
        api_request_logs) would eventually try to load the entire
        table into memory and serialize it in one response."""

        return self.repository.get_all(db=db, skip=skip, limit=limit)

    def update(
        self,
        db: Session,
        obj: Any,
        data: Any,
    ) -> Any:
        """Update an existing record."""

        update_data = data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(obj, field, value)

        return self.repository.save(
            db=db,
            obj=obj,
        )

    def delete(
        self,
        db: Session,
        obj: Any,
    ) -> None:
        """Delete an existing record."""

        self.repository.delete(
            db=db,
            obj=obj,
        )