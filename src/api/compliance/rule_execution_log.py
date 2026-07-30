from fastapi import APIRouter, Depends, status

from src.api.dependencies.compliance import (
    get_rule_execution_log_service,
)
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
async def create_rule_execution_log(
    data: RuleExecutionLogCreate,
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return await service.create_rule_execution_log(data)


@router.get(
    "/",
    response_model=list[RuleExecutionLogResponse],
)
async def get_rule_execution_logs(
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> list[RuleExecutionLog]:
    return await service.get_rule_execution_logs()


@router.get(
    "/{rule_execution_log_id}",
    response_model=RuleExecutionLogResponse,
)
async def get_rule_execution_log(
    rule_execution_log_id: int,
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return await service.get_rule_execution_log(
        rule_execution_log_id,
    )


@router.put(
    "/{rule_execution_log_id}",
    response_model=RuleExecutionLogResponse,
)
async def update_rule_execution_log(
    rule_execution_log_id: int,
    data: RuleExecutionLogUpdate,
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> RuleExecutionLog:
    return await service.update_rule_execution_log(
        rule_execution_log_id,
        data,
    )


@router.delete(
    "/{rule_execution_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_rule_execution_log(
    rule_execution_log_id: int,
    service: RuleExecutionLogService = Depends(
        get_rule_execution_log_service,
    ),
) -> None:
    await service.delete_rule_execution_log(
        rule_execution_log_id,
    )