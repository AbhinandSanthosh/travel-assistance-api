from fastapi import Depends, FastAPI

from src.api.dependencies.auth import get_current_user
from src.api.handlers import register_exception_handlers
from src.api.reference.country import router as country_router
from src.config.settings import settings
from src.api.reference.region import router as region_router
from src.api.reference.currency import router as currency_router
from src.api.reference.passport_type import (
    router as passport_type_router,
)
from src.api.reference.visa_type import router as visa_type_router
from src.api.reference.airline import router as airline_router
from src.api.reference.airport import router as airport_router
from src.api.reference.purpose import router as purpose_router
from src.api.reference.passenger_type import (
    router as passenger_type_router,
)
from src.api.reference.travel_authorization import (
    router as travel_authorization_router,
)

from src.api.compliance.rule import router as rule_router

from src.api.compliance.visa_rule import router as visa_rule_router

from src.api.compliance.travel_authorization_rule import (
    router as travel_authorization_rule_router,
)
from src.api.compliance.passport_rule import router as passport_rule_router

from src.api.compliance.transit_rule import (
    router as transit_rule_router,
)
from src.api.compliance.health_rule import (
    router as health_rule_router,
)
from src.api.compliance.vaccine import (
    router as vaccine_router,
)
from src.api.compliance.health_rule_vaccine import (
    router as health_rule_vaccine_router,
)
from src.api.compliance.immigration_rule import (
    router as immigration_rule_router,
)
from src.api.compliance.customs_rule import (
    router as customs_rule_router,
)
from src.api.compliance.entry_restriction import (
    router as entry_restriction_router,
)

from src.api.administration.auth import router as auth_router
from src.api.administration.role import router as role_router
from src.api.administration.permission import (
    router as permission_router,
)
from src.api.administration.role_permission import (
    router as role_permission_router,
)
from src.api.administration.user import (
    router as user_router,
)
from src.api.rule_management.rule_status import (
    router as rule_status_router,
)
from src.api.rule_management.rule_version import (
    router as rule_version_router,
)
from src.api.rule_management.rule_history import (
    router as rule_history_router,
)
from src.api.rule_management.rule_approval import router as rule_approval_router

from src.api.rule_management.rule_simulation import (
    router as rule_simulation_router,
)
from src.api.administration.api_client import (
    router as api_client_router,
)
from src.api.administration.client_ip_whitelist import (
    router as client_ip_whitelist_router,
)
from src.api.administration.client_portal import (
    router as client_portal_router,
)
from src.api.administration.audit_log import (
    router as audit_log_router,
)
from src.api.administration.api_request_log import (
    router as api_request_log_router,
)
from src.api.administration.client_usage_statistics import (
    router as client_usage_statistics_router,
)
from src.api.data_collection.source_registry import (
    router as source_registry_router,
)
from src.api.data_collection.source_document import (
    router as source_document_router,
)
from src.api.data_collection.document_version import (
    router as document_version_router,
)
from src.api.data_collection.collection_log import (
    router as collection_log_router,
)
from src.api.data_collection.document_validation import (
    router as document_validation_router,
)
from src.api.data_collection.ai_extraction import (
    router as ai_extraction_router,
)
from src.api.compliance.compliance_check import (
    router as compliance_check_router,
)
from src.api.compliance.rule_execution_log import (
    router as rule_execution_log_router,
)
from src.api.compliance.autocheck import (
    router as autocheck_router,
)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# Register global exception handlers
register_exception_handlers(app)

# ---------------------------------------------------------------------------
# Admin API (JWT protected) -- every router below requires a valid Bearer
# token obtained from POST /api/v1/auth/login. Used by Compliance Officers,
# Administrators, and internal staff to manage reference data, travel rules,
# rule lifecycle, API clients, and system users.
# ---------------------------------------------------------------------------
_admin_auth = [Depends(get_current_user)]

app.include_router(auth_router)

app.include_router(country_router)
app.include_router(region_router, dependencies=_admin_auth)
app.include_router(currency_router, dependencies=_admin_auth)
app.include_router(passport_type_router)
app.include_router(visa_type_router, dependencies=_admin_auth)
app.include_router(airline_router, dependencies=_admin_auth)
app.include_router(airport_router, dependencies=_admin_auth)
app.include_router(purpose_router)
app.include_router(passenger_type_router, dependencies=_admin_auth)
app.include_router(travel_authorization_router, dependencies=_admin_auth)

app.include_router(rule_router, dependencies=_admin_auth)
app.include_router(visa_rule_router, dependencies=_admin_auth)
app.include_router(
    travel_authorization_rule_router,
    dependencies=_admin_auth,
)
app.include_router(passport_rule_router, dependencies=_admin_auth)
app.include_router(
    transit_rule_router,
    dependencies=_admin_auth,
)
app.include_router(
    health_rule_router,
    dependencies=_admin_auth,
)
app.include_router(
    vaccine_router,
    dependencies=_admin_auth,
)
app.include_router(
    health_rule_vaccine_router,
    dependencies=_admin_auth,
)
app.include_router(
    immigration_rule_router,
    dependencies=_admin_auth,
)
app.include_router(
    customs_rule_router,
    dependencies=_admin_auth,
)
app.include_router(
    entry_restriction_router,
    dependencies=_admin_auth,
)
app.include_router(compliance_check_router, dependencies=_admin_auth)
app.include_router(rule_execution_log_router, dependencies=_admin_auth)

app.include_router(role_router, dependencies=_admin_auth)
app.include_router(permission_router, dependencies=_admin_auth)
app.include_router(role_permission_router, dependencies=_admin_auth)
app.include_router(user_router, dependencies=_admin_auth)
app.include_router(api_client_router, dependencies=_admin_auth)
app.include_router(client_ip_whitelist_router, dependencies=_admin_auth)
app.include_router(audit_log_router, dependencies=_admin_auth)
app.include_router(api_request_log_router, dependencies=_admin_auth)
app.include_router(client_usage_statistics_router, dependencies=_admin_auth)
app.include_router(client_portal_router)

app.include_router(source_registry_router, dependencies=_admin_auth)
app.include_router(source_document_router, dependencies=_admin_auth)
app.include_router(document_version_router, dependencies=_admin_auth)
app.include_router(collection_log_router, dependencies=_admin_auth)
app.include_router(document_validation_router, dependencies=_admin_auth)
app.include_router(ai_extraction_router, dependencies=_admin_auth)

app.include_router(rule_status_router, dependencies=_admin_auth)
app.include_router(rule_version_router, dependencies=_admin_auth)
app.include_router(rule_history_router, dependencies=_admin_auth)
app.include_router(rule_approval_router, dependencies=_admin_auth)
app.include_router(rule_simulation_router, dependencies=_admin_auth)

# ---------------------------------------------------------------------------
# Client API (API Key protected) -- authenticated via X-API-Key inside
# AutoCheckService itself (validates api_clients.api_key, client status,
# IP whitelist, and rate limit). No JWT dependency here: this is the
# endpoint airlines / booking platforms / travel agencies call directly.
# ---------------------------------------------------------------------------
app.include_router(autocheck_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Travel Assistance API is running",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
    }
