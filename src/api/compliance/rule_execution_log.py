from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.compliance import (
    get_rule_execution_log_service,
)
from src.db.session import get_db
from src.models.compliance.rule_execution_log import (
    RuleExecutionLog,
)
from src.schemas.compliance.rule_execution_log import (
    RuleExecutionLogCreate,
    RuleExecutionLogResponse,
    RuleExecutionLogUpdate,
)
from src.services.compliance.rule_execution_log import (
    RuleExecutionLogService,
)

router = APIRouter(
    prefix="/rule-execution-logs",
    tags=["Rule Execution Logs"],
)


@router.post(
    "/",
    response_model=RuleExecutionLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rule_execution_log(
    data: RuleExecutionLogCreate,
    db: Session = Depends(get_db),
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return service.create_rule_execution_log(
        db=db,
        rule_execution_log_data=data,
    )


@router.get(
    "/",
    response_model=list[RuleExecutionLogResponse],
)
def get_rule_execution_logs(
    db: Session = Depends(get_db),
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> list[RuleExecutionLog]:
    return service.get_rule_execution_logs(db)


@router.get(
    "/{rule_execution_log_id}",
    response_model=RuleExecutionLogResponse,
)
def get_rule_execution_log(
    rule_execution_log_id: int,
    db: Session = Depends(get_db),
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return service.get_rule_execution_log(
        db=db,
        rule_execution_log_id=rule_execution_log_id,
    )


@router.put(
    "/{rule_execution_log_id}",
    response_model=RuleExecutionLogResponse,
)
def update_rule_execution_log(
    rule_execution_log_id: int,
    data: RuleExecutionLogUpdate,
    db: Session = Depends(get_db),
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return service.update_rule_execution_log(
        db=db,
        rule_execution_log_id=rule_execution_log_id,
        rule_execution_log_data=data,
    )


@router.delete(
    "/{rule_execution_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rule_execution_log(
    rule_execution_log_id: int,
    db: Session = Depends(get_db),
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> None:
    service.delete_rule_execution_log(
        db=db,
        rule_execution_log_id=rule_execution_log_id,
    )