from fastapi import Depends
from src.api.dependencies.administration import (
    get_api_client_repository,
    get_api_request_log_service,
    get_client_ip_whitelist_service,
)
from src.core.redis_client import get_redis_client
from src.repositories.administration.api_client import APIClientRepository
from src.services.administration.api_request_log import APIRequestLogService
from src.services.administration.client_ip_whitelist import ClientIPWhitelistService
from src.services.compliance.compliance_check import ComplianceCheckService
from src.services.compliance.rule_execution_log import RuleExecutionLogService
from src.api.dependencies.compliance import get_compliance_check_service, get_rule_execution_log_service
from src.services.v1.travel_requirements_service import TravelRequirementsService

def get_travel_requirements_service(
    api_client_repository: APIClientRepository = Depends(get_api_client_repository),
    client_ip_whitelist_service: ClientIPWhitelistService = Depends(get_client_ip_whitelist_service),
    api_request_log_service: APIRequestLogService = Depends(get_api_request_log_service),
    compliance_check_service: ComplianceCheckService = Depends(get_compliance_check_service),
    rule_execution_log_service: RuleExecutionLogService = Depends(get_rule_execution_log_service),
) -> TravelRequirementsService:
    return TravelRequirementsService(
        api_client_repository,
        client_ip_whitelist_service,
        api_request_log_service,
        compliance_check_service,
        rule_execution_log_service,
        get_redis_client(),
    )
