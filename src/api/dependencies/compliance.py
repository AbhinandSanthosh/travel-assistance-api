from fastapi import Depends

from src.repositories.compliance.rule import RuleRepository
from src.services.compliance.rule import RuleService


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