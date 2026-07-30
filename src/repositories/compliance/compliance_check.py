from src.models.compliance.compliance_check import (
    ComplianceCheck,
)
from src.repositories.base_repository import BaseRepository


class ComplianceCheckRepository(
    BaseRepository[ComplianceCheck]
):
    """Repository for Compliance Check."""

    def __init__(self) -> None:
        super().__init__(ComplianceCheck)

    async def get_by_request_id(
        self,
        request_id: str,
    ) -> ComplianceCheck | None:
        return await self.get_by_fields(
            request_id=request_id,
        )