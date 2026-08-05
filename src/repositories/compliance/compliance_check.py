from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.compliance_check import (
    ComplianceCheck,
)
from src.repositories.base_repository import (
    BaseRepository,
)


class ComplianceCheckRepository(
    BaseRepository[ComplianceCheck],
):
    """Repository for ComplianceCheck."""

    def __init__(self) -> None:
        super().__init__(ComplianceCheck)

    def get_by_request_id(
        self,
        db: Session,
        request_id: str,
    ) -> ComplianceCheck | None:
        return db.scalar(
            select(ComplianceCheck).where(
                ComplianceCheck.request_id == request_id,
            )
        )