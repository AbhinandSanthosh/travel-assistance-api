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

from src.repositories.reference.airline_repository import (
    AirlineRepository,
)
from src.services.reference.airline_service import (
    AirlineService,
)

from src.repositories.reference.airport_repository import (
    AirportRepository,
)
from src.services.reference.airport_service import (
    AirportService,
)

from src.repositories.reference.purpose_repository import (
    PurposeRepository,
)
from src.services.reference.purpose_service import (
    PurposeService,
)

from src.repositories.reference.passenger_type_repository import (
    PassengerTypeRepository,
)
from src.services.reference.passenger_type_service import (
    PassengerTypeService,
)

from src.repositories.reference.travel_authorization_repository import (
    TravelAuthorizationRepository,
)
from src.services.reference.travel_authorization_service import (
    TravelAuthorizationService,
)
from src.repositories.reference.city_repository import (
    CityRepository,
)
from src.services.reference.city_service import (
    CityService,
)

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

def get_airline_repository() -> AirlineRepository:
    """Get Airline repository instance."""
    return AirlineRepository()

def get_airline_service(
    airline_repository: AirlineRepository = Depends(
        get_airline_repository,
    ),
    country_repository: CountryRepository = Depends(
        get_country_repository,
    ),
) -> AirlineService:
    """Get Airline service instance."""
    return AirlineService(
        airline_repository,
        country_repository,
    )

def get_airport_repository() -> AirportRepository:
    """Get Airport repository instance."""
    return AirportRepository()

def get_airport_service(
    airport_repository: AirportRepository = Depends(
        get_airport_repository,
    ),
    country_repository: CountryRepository = Depends(
        get_country_repository,
    ),
) -> AirportService:
    """Get Airport service instance."""
    return AirportService(
        airport_repository,
        country_repository,
    )

def get_city_repository() -> CityRepository:
    """Get City repository instance."""
    return CityRepository()

def get_city_service(
    city_repository: CityRepository = Depends(
        get_city_repository,
    ),
    country_repository: CountryRepository = Depends(
        get_country_repository,
    ),
) -> CityService:
    """Get City service instance."""
    return CityService(
        city_repository,
        country_repository,
    )

def get_purpose_repository() -> PurposeRepository:
    """Get Purpose repository instance."""
    return PurposeRepository()

def get_purpose_service(
    purpose_repository: PurposeRepository = Depends(
        get_purpose_repository,
    ),
) -> PurposeService:
    """Get Purpose service instance."""
    return PurposeService(
        purpose_repository,
    )

def get_passenger_type_repository() -> PassengerTypeRepository:
    """Get PassengerType repository."""

    return PassengerTypeRepository()


def get_passenger_type_service(
    passenger_type_repository: PassengerTypeRepository = Depends(
        get_passenger_type_repository,
    ),
) -> PassengerTypeService:
    """Get PassengerType service."""

    return PassengerTypeService(
        passenger_type_repository,
    )

def get_travel_authorization_repository(
) -> TravelAuthorizationRepository:
    """Get TravelAuthorization repository."""

    return TravelAuthorizationRepository()


def get_travel_authorization_service(
    travel_authorization_repository: TravelAuthorizationRepository = Depends(
        get_travel_authorization_repository,
    ),
    country_repository: CountryRepository = Depends(
        get_country_repository,
    ),
) -> TravelAuthorizationService:
    """Get TravelAuthorization service."""

    return TravelAuthorizationService(
        travel_authorization_repository,
        country_repository,
    )