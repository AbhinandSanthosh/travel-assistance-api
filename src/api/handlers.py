from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.base import AppException
from src.exceptions.country import (
    CountryAlreadyExistsError,
    CountryNotFoundError,
)

from src.exceptions.region import (
    RegionAlreadyExistsError,
    RegionNotFoundError,
)

from src.exceptions.currency import (
    CurrencyAlreadyExistsError,
    CurrencyNotFoundError,
)

from src.exceptions.passport_type import (
    PassportTypeAlreadyExistsError,
    PassportTypeNotFoundError,
)

from src.exceptions.visa_type import (
    VisaTypeAlreadyExistsError,
    VisaTypeNotFoundError,
)

def register_exception_handlers(app: FastAPI) -> None:
    """Register application exception handlers."""

    @app.exception_handler(CountryAlreadyExistsError)
    async def country_already_exists_handler(
        request: Request,
        exc: CountryAlreadyExistsError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CountryNotFoundError)
    async def country_not_found_handler(
        request: Request,
        exc: CountryNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RegionAlreadyExistsError)
    async def region_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )


    @app.exception_handler(RegionNotFoundError)
    async def region_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CurrencyAlreadyExistsError)
    async def currency_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )


    @app.exception_handler(CurrencyNotFoundError)
    async def currency_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PassportTypeAlreadyExistsError)
    async def passport_type_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )


    @app.exception_handler(PassportTypeNotFoundError)
    async def passport_type_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(VisaTypeAlreadyExistsError)
    async def visa_type_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )


    @app.exception_handler(VisaTypeNotFoundError)
    async def visa_type_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )