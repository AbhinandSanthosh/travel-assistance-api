from fastapi import Depends


from src.repositories.reference.country_repository import CountryRepository
from src.services.reference.country_service import CountryService

from src.repositories.reference.region_repository import RegionRepository
from src.services.reference.region_service import RegionService

from src.repositories.reference.currency_repository import CurrencyRepository
from src.services.reference.currency_service import CurrencyService

from src.repositories.reference.passport_type_repository import (
    PassportTypeRepository,
)
from src.services.reference.passport_type_service import (
    PassportTypeService,
)

from src.repositories.reference.visa_type_repository import VisaTypeRepository
from src.services.reference.visa_type import VisaTypeService

def get_country_repository() -> CountryRepository:
    """Provide a CountryRepository instance."""
    return CountryRepository()


def get_region_repository() -> RegionRepository:
    """Get Region repository instance."""
    return RegionRepository()


def get_region_service(
    region_repository: RegionRepository = Depends(get_region_repository),
) -> RegionService:
    """Get Region service instance."""
    return RegionService(region_repository)

def get_currency_repository() -> CurrencyRepository:
    """Get Currency repository instance."""
    return CurrencyRepository()


def get_currency_service(
    currency_repository: CurrencyRepository = Depends(get_currency_repository),
) -> CurrencyService:
    """Get Currency service instance."""
    return CurrencyService(currency_repository)

def get_country_service(
    country_repository: CountryRepository = Depends(get_country_repository),
    region_repository: RegionRepository = Depends(get_region_repository),
    currency_repository: CurrencyRepository = Depends(get_currency_repository),
) -> CountryService:
    """Get Country service instance."""
    return CountryService(
        country_repository,
        region_repository,
        currency_repository,
    )

def get_passport_type_repository() -> PassportTypeRepository:
    """Get PassportType repository instance."""
    return PassportTypeRepository()


def get_passport_type_service(
    passport_type_repository: PassportTypeRepository = Depends(
        get_passport_type_repository,
    ),
) -> PassportTypeService:
    """Get PassportType service instance."""
    return PassportTypeService(passport_type_repository)

def get_visa_type_repository() -> VisaTypeRepository:
    """Get VisaType repository instance."""
    return VisaTypeRepository()

def get_visa_type_service(
    visa_type_repository: VisaTypeRepository = Depends(
        get_visa_type_repository,
    ),
) -> VisaTypeService:
    return VisaTypeService(
        visa_type_repository,
    )