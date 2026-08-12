from fastapi import Depends


from src.repositories.administration.role import RoleRepository
from src.services.administration.role import RoleService


from src.repositories.administration.permission import (
    PermissionRepository,
)
from src.services.administration.permission import (
    PermissionService,
)


from src.repositories.administration.role_permission import (
    RolePermissionRepository,
)
from src.services.administration.role_permission import (
    RolePermissionService,
)
from src.repositories.administration.user import (
    UserRepository,
)


from src.services.administration.user import (
    UserService,
)
from src.repositories.administration.api_client import (
    APIClientRepository,
)
from src.services.administration.api_client import (
    APIClientService,
)
from src.repositories.administration.client_ip_whitelist import (
    ClientIPWhitelistRepository,
)
from src.services.administration.client_ip_whitelist import (
    ClientIPWhitelistService,
)
from src.repositories.administration.audit_log import (
    AuditLogRepository,
)
from src.services.administration.audit_log import (
    AuditLogService,
)
from src.repositories.administration.api_request_log import (
    APIRequestLogRepository,
)
from src.services.administration.api_request_log import (
    APIRequestLogService,
)
from src.repositories.administration.client_usage_statistics import (
    ClientUsageStatisticsRepository,
)
from src.services.administration.client_usage_statistics import (
    ClientUsageStatisticsService,
)
from src.services.administration.client_portal_service import (
    ClientPortalService,
)


def get_role_repository() -> RoleRepository:
    """Get Role repository instance."""
    return RoleRepository()


def get_role_service(
    role_repository: RoleRepository = Depends(
        get_role_repository,
    ),
) -> RoleService:
    """Get Role service instance."""
    return RoleService(
        role_repository,
    )


def get_permission_repository() -> PermissionRepository:
    """Get Permission repository instance."""
    return PermissionRepository()


def get_permission_service(
    permission_repository: PermissionRepository = Depends(
        get_permission_repository,
    ),
) -> PermissionService:
    """Get Permission service instance."""
    return PermissionService(
        permission_repository,
    )


def get_role_permission_repository() -> RolePermissionRepository:
    """Get RolePermission repository instance."""
    return RolePermissionRepository()


def get_role_permission_service(
    role_permission_repository: RolePermissionRepository = Depends(
        get_role_permission_repository,
    ),
    role_repository: RoleRepository = Depends(
        get_role_repository,
    ),
    permission_repository: PermissionRepository = Depends(
        get_permission_repository,
    ),
) -> RolePermissionService:
    """Get RolePermission service instance."""
    return RolePermissionService(
        role_permission_repository,
        role_repository,
        permission_repository,
    )


def get_user_repository() -> UserRepository:
    """Get User repository instance."""
    return UserRepository()


def get_user_service(
    user_repository: UserRepository = Depends(
        get_user_repository,
    ),
    role_repository: RoleRepository = Depends(
        get_role_repository,
    ),
) -> UserService:
    """Get User service instance."""
    return UserService(
        user_repository,
        role_repository,
    )


def get_api_client_repository() -> APIClientRepository:
    """Get API Client repository."""
    return APIClientRepository()


def get_api_client_service(
    repository: APIClientRepository = Depends(
        get_api_client_repository,
    ),
) -> APIClientService:
    """Get API Client service."""
    return APIClientService(repository)


def get_client_ip_whitelist_repository() -> ClientIPWhitelistRepository:
    """Get Client IP Whitelist repository."""
    return ClientIPWhitelistRepository()


def get_client_portal_service(
    repository: APIClientRepository = Depends(
        get_api_client_repository,
    ),
    whitelist_repository: ClientIPWhitelistRepository = Depends(
        get_client_ip_whitelist_repository,
    ),
) -> ClientPortalService:
    """Get Client Portal service."""
    return ClientPortalService(
        repository,
        whitelist_repository,
    )


def get_client_ip_whitelist_service(
    repository: ClientIPWhitelistRepository = Depends(
        get_client_ip_whitelist_repository,
    ),
) -> ClientIPWhitelistService:
    """Get Client IP Whitelist service."""
    return ClientIPWhitelistService(repository)


def get_audit_log_repository() -> AuditLogRepository:
    """Get Audit Log repository."""
    return AuditLogRepository()


def get_audit_log_service(
    repository: AuditLogRepository = Depends(
        get_audit_log_repository,
    ),
) -> AuditLogService:
    """Get Audit Log service."""
    return AuditLogService(repository)


def get_api_request_log_repository() -> APIRequestLogRepository:
    """Get API Request Log repository."""
    return APIRequestLogRepository()


def get_api_request_log_service(
    repository: APIRequestLogRepository = Depends(
        get_api_request_log_repository,
    ),
) -> APIRequestLogService:
    """Get API Request Log service."""
    return APIRequestLogService(repository)


def get_client_usage_statistics_repository() -> ClientUsageStatisticsRepository:
    """Get Client Usage Statistics repository."""
    return ClientUsageStatisticsRepository()


def get_client_usage_statistics_service(
    repository: ClientUsageStatisticsRepository = Depends(
        get_client_usage_statistics_repository,
    ),
) -> ClientUsageStatisticsService:
    """Get Client Usage Statistics service."""
    return ClientUsageStatisticsService(repository)