from fastapi import FastAPI

from src.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


@app.get("/")
def root():
    return {
        "message": "Travel Assistance API is running",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }