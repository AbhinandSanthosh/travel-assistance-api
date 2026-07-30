from src.exceptions.compliance.compliance_check import (
    ComplianceCheckNotFoundError,
    ComplianceCheckRequestIdAlreadyExistsError,
)
from src.models.compliance.compliance_check import (
    ComplianceCheck,
)
from src.repositories.compliance.compliance_check import (
    ComplianceCheckRepository,
)
from src.schemas.compliance.compliance_check import (
    ComplianceCheckCreate,
    ComplianceCheckUpdate,
)
from src.services.base_crud_service import BaseCrudService


class ComplianceCheckService:
    """Service for Compliance Check."""

    def __init__(
        self,
        repository: ComplianceCheckRepository,
    ) -> None:
        self.repository = repository
        self.base_crud = BaseCrudService(
            repository,
        )

    async def create_compliance_check(
        self,
        data: ComplianceCheckCreate,
    ) -> ComplianceCheck:
        existing = await self.repository.get_by_request_id(
            data.request_id,
        )

        if existing is not None:
            raise (
                ComplianceCheckRequestIdAlreadyExistsError()
            )

        return await self.base_crud.create(data)

    async def get_compliance_check(
        self,
        compliance_check_id: int,
    ) -> ComplianceCheck:
        compliance_check = (
            await self.base_crud.get_by_id(
                compliance_check_id,
            )
        )

        if compliance_check is None:
            raise ComplianceCheckNotFoundError()

        return compliance_check

    async def get_compliance_checks(
        self,
    ) -> list[ComplianceCheck]:
        return await self.base_crud.get_all()

    async def update_compliance_check(
        self,
        compliance_check_id: int,
        data: ComplianceCheckUpdate,
    ) -> ComplianceCheck:
        compliance_check = (
            await self.base_crud.get_by_id(
                compliance_check_id,
            )
        )

        if compliance_check is None:
            raise ComplianceCheckNotFoundError()

        return await self.base_crud.update(
            compliance_check,
            data,
        )

    async def delete_compliance_check(
        self,
        compliance_check_id: int,
    ) -> None:
        compliance_check = (
            await self.base_crud.get_by_id(
                compliance_check_id,
            )
        )

        if compliance_check is None:
            raise ComplianceCheckNotFoundError()

        await self.base_crud.delete(
            compliance_check,
        )