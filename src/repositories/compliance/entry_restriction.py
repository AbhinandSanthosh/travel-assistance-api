from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.entry_restriction import (
    EntryRestriction,
)
from src.repositories.base_repository import (
    BaseRepository,
)


class EntryRestrictionRepository(
    BaseRepository[EntryRestriction],
):
    """Repository for EntryRestriction-specific database operations."""

    def __init__(self) -> None:
        super().__init__(EntryRestriction)

    def get_by_rule_id(
        self,
        db: Session,
        rule_id: int,
    ) -> EntryRestriction | None:
        return db.scalar(
            select(EntryRestriction).where(
                EntryRestriction.rule_id == rule_id
            )
        )