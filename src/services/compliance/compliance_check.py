from sqlalchemy.orm import Session

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
from src.services.base_crud_service import (
    BaseCrudService,
)


class ComplianceCheckService:
    """Service layer for ComplianceCheck."""

    def __init__(
        self,
        repository: ComplianceCheckRepository,
    ) -> None:
        self.repository = repository
        self.crud = BaseCrudService(repository)

    def create_compliance_check(
        self,
        db: Session,
        data: ComplianceCheckCreate,
    ) -> ComplianceCheck:

        if (
            self.repository.get_by_request_id(
                db,
                data.request_id,
            )
            is not None
        ):
            raise ComplianceCheckRequestIdAlreadyExistsError()

        return self.crud.create(
            db=db,
            model=ComplianceCheck,
            data=data,
        )

    def get_compliance_check(
        self,
        db: Session,
        compliance_check_id: int,
    ) -> ComplianceCheck:

        obj = self.crud.get_by_id(
            db=db,
            obj_id=compliance_check_id,
        )

        if obj is None:
            raise ComplianceCheckNotFoundError()

        return obj

    def get_compliance_checks(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ComplianceCheck]:
        return self.crud.get_all(db, skip, limit)

    def update_compliance_check(
        self,
        db: Session,
        compliance_check_id: int,
        data: ComplianceCheckUpdate,
    ) -> ComplianceCheck:

        obj = self.get_compliance_check(
            db,
            compliance_check_id,
        )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if (
            "request_id" in update_data
            and update_data["request_id"]
            != obj.request_id
        ):
            existing = self.repository.get_by_request_id(
                db,
                update_data["request_id"],
            )

            if existing is not None:
                raise ComplianceCheckRequestIdAlreadyExistsError()

        return self.crud.update(
            db=db,
            obj=obj,
            data=data,
        )

    def delete_compliance_check(
        self,
        db: Session,
        compliance_check_id: int,
    ) -> None:

        obj = self.get_compliance_check(
            db,
            compliance_check_id,
        )

        self.crud.delete(
            db=db,
            obj=obj,
        )