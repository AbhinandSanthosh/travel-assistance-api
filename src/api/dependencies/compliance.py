from fastapi import Depends

from src.repositories.compliance.rule import RuleRepository
from src.services.compliance.rule import RuleService

from src.repositories.compliance.visa_rule import VisaRuleRepository
from src.services.compliance.visa_rule import VisaRuleService

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