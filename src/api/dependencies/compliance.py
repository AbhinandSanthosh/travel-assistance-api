from fastapi import Depends

from src.repositories.compliance.rule import RuleRepository
from src.services.compliance.rule import RuleService

from src.repositories.compliance.visa_rule import VisaRuleRepository
from src.services.compliance.visa_rule import VisaRuleService

from src.repositories.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleRepository,
)
from src.services.compliance.travel_authorization_rule import (
    TravelAuthorizationRuleService,
)

from src.repositories.compliance.passport_rule import (
    PassportRuleRepository,
)
from src.services.compliance.passport_rule import (
    PassportRuleService,
)

from src.repositories.compliance.transit_rule import (
    TransitRuleRepository,
)
from src.services.compliance.transit_rule import (
    TransitRuleService,
)

from src.repositories.compliance.health_rule import (
    HealthRuleRepository,
)
from src.services.compliance.health_rule import (
    HealthRuleService,
)

from src.repositories.compliance.vaccine import (
    VaccineRepository,
)
from src.services.compliance.vaccine import (
    VaccineService,
)
from src.repositories.compliance.health_rule_vaccine import (
    HealthRuleVaccineRepository,
)
from src.services.compliance.health_rule_vaccine import (
    HealthRuleVaccineService,
)
from src.repositories.compliance.immigration_rule import (
    ImmigrationRuleRepository,
)
from src.services.compliance.immigration_rule import (
    ImmigrationRuleService,
)
from src.repositories.compliance.customs_rule import (
    CustomsRuleRepository,
)
from src.services.compliance.customs_rule import (
    CustomsRuleService,
)
from src.repositories.compliance.entry_restriction import (
    EntryRestrictionRepository,
)
from src.services.compliance.entry_restriction import (
    EntryRestrictionService,
)

def get_rule_repository() -> RuleRepository:
    """Get Rule repository instance."""
    return RuleRepository()


def get_rule_service(
    rule_repository: RuleRepository = Depends(
        get_rule_repository,
    ),
) -> RuleService:
    """Get Rule service instance."""
    return RuleService(
        rule_repository,
    )

def get_visa_rule_repository() -> VisaRuleRepository:
    """Get VisaRule repository instance."""
    return VisaRuleRepository()


def get_visa_rule_service(
    visa_rule_repository: VisaRuleRepository = Depends(
        get_visa_rule_repository,
    ),
) -> VisaRuleService:
    """Get VisaRule service instance."""
    return VisaRuleService(
        visa_rule_repository,
    )

def get_travel_authorization_rule_repository(
) -> TravelAuthorizationRuleRepository:
    """Get TravelAuthorizationRule repository instance."""
    return TravelAuthorizationRuleRepository()


def get_travel_authorization_rule_service(
    travel_authorization_rule_repository: (
        TravelAuthorizationRuleRepository
    ) = Depends(
        get_travel_authorization_rule_repository,
    ),
) -> TravelAuthorizationRuleService:
    """Get TravelAuthorizationRule service instance."""
    return TravelAuthorizationRuleService(
        travel_authorization_rule_repository,
    )

def get_passport_rule_repository() -> PassportRuleRepository:
    """Get PassportRule repository instance."""
    return PassportRuleRepository()


def get_passport_rule_service(
    passport_rule_repository: PassportRuleRepository = Depends(
        get_passport_rule_repository,
    ),
) -> PassportRuleService:
    """Get PassportRule service instance."""
    return PassportRuleService(
        passport_rule_repository,
    )

def get_transit_rule_repository() -> TransitRuleRepository:
    """Get TransitRule repository instance."""
    return TransitRuleRepository()


def get_transit_rule_service(
    transit_rule_repository: TransitRuleRepository = Depends(
        get_transit_rule_repository,
    ),
) -> TransitRuleService:
    """Get TransitRule service instance."""
    return TransitRuleService(
        transit_rule_repository,
    )

def get_health_rule_repository() -> HealthRuleRepository:
    """Get HealthRule repository instance."""
    return HealthRuleRepository()


def get_health_rule_service(
    health_rule_repository: HealthRuleRepository = Depends(
        get_health_rule_repository,
    ),
) -> HealthRuleService:
    """Get HealthRule service instance."""
    return HealthRuleService(
        health_rule_repository,
    )

def get_vaccine_repository() -> VaccineRepository:
    """Get Vaccine repository instance."""
    return VaccineRepository()


def get_vaccine_service(
    vaccine_repository: VaccineRepository = Depends(
        get_vaccine_repository,
    ),
) -> VaccineService:
    """Get Vaccine service instance."""
    return VaccineService(
        vaccine_repository,
    )

def get_health_rule_vaccine_repository(
) -> HealthRuleVaccineRepository:
    """Get HealthRuleVaccine repository instance."""
    return HealthRuleVaccineRepository()


def get_health_rule_vaccine_service(
    health_rule_vaccine_repository: (
        HealthRuleVaccineRepository
    ) = Depends(
        get_health_rule_vaccine_repository,
    ),
) -> HealthRuleVaccineService:
    """Get HealthRuleVaccine service instance."""
    return HealthRuleVaccineService(
        health_rule_vaccine_repository,
    )

def get_immigration_rule_repository(
) -> ImmigrationRuleRepository:
    """Get ImmigrationRule repository instance."""
    return ImmigrationRuleRepository()


def get_immigration_rule_service(
    immigration_rule_repository: (
        ImmigrationRuleRepository
    ) = Depends(
        get_immigration_rule_repository,
    ),
) -> ImmigrationRuleService:
    """Get ImmigrationRule service instance."""
    return ImmigrationRuleService(
        immigration_rule_repository,
    )

def get_customs_rule_repository(
) -> CustomsRuleRepository:
    """Get CustomsRule repository instance."""
    return CustomsRuleRepository()


def get_customs_rule_service(
    customs_rule_repository: (
        CustomsRuleRepository
    ) = Depends(
        get_customs_rule_repository,
    ),
) -> CustomsRuleService:
    """Get CustomsRule service instance."""
    return CustomsRuleService(
        customs_rule_repository,
    )

def get_entry_restriction_repository(
) -> EntryRestrictionRepository:
    """Get EntryRestriction repository instance."""
    return EntryRestrictionRepository()


def get_entry_restriction_service(
    entry_restriction_repository: (
        EntryRestrictionRepository
    ) = Depends(
        get_entry_restriction_repository,
    ),
) -> EntryRestrictionService:
    """Get EntryRestriction service instance."""
    return EntryRestrictionService(
        entry_restriction_repository,
    )