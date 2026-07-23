from fastapi import FastAPI

from src.api.handlers import register_exception_handlers
from src.api.reference.country import router as country_router
from src.config.settings import settings
from src.api.reference.region import router as region_router
from src.api.reference.currency import router as currency_router
from src.api.reference.passport_type import (
    router as passport_type_router,
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