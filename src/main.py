from fastapi import FastAPI

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

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# Register global exception handlers
register_exception_handlers(app)

# Register API routers
app.include_router(country_router)
app.include_router(region_router)
app.include_router(currency_router)
app.include_router(passport_type_router)
app.include_router(visa_type_router)
app.include_router(airline_router)
app.include_router(airport_router)
app.include_router(purpose_router)
app.include_router(passenger_type_router)
app.include_router(travel_authorization_router)

app.include_router(rule_router)
app.include_router(visa_rule_router)
app.include_router(
    travel_authorization_rule_router,
)
app.include_router(passport_rule_router)
app.include_router(
    transit_rule_router,
)
app.include_router(
    health_rule_router,
)
app.include_router(
    vaccine_router,
)
app.include_router(
    health_rule_vaccine_router,
)
app.include_router(
    immigration_rule_router,
)
app.include_router(
    customs_rule_router,
)
app.include_router(
    entry_restriction_router,
)

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