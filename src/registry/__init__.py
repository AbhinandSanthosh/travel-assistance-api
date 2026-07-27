from src.models.reference.airline import Airline
from src.models.reference.airport import Airport
from src.models.reference.country import Country
from src.models.reference.currency import Currency
from src.models.reference.passenger_type import PassengerType
from src.models.reference.passport_type import PassportType
from src.models.reference.purpose import Purpose
from src.models.reference.region import Region
from src.models.reference.travel_authorization import TravelAuthorization
from src.models.reference.visa_type import VisaType


REFERENCE_MODELS = {
    "airline": Airline,
    "airport": Airport,
    "country": Country,
    "currency": Currency,
    "passenger_type": PassengerType,
    "passport_type": PassportType,
    "purpose": Purpose,
    "region": Region,
    "travel_authorization": TravelAuthorization,
    "visa_type": VisaType,
}