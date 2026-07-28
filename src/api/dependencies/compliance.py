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