from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.compliance.health_rule_vaccine import (
    HealthRuleVaccine,
)
from src.repositories.base_repository import BaseRepository


class HealthRuleVaccineRepository(
    BaseRepository[HealthRuleVaccine],
):
    """Repository for HealthRuleVaccine-specific database operations."""

    def __init__(self) -> None:
        super().__init__(HealthRuleVaccine)

    def get_by_health_rule_and_vaccine(
        self,
        db: Session,
        health_rule_id: int,
        vaccine_id: int,
    ) -> HealthRuleVaccine | None:
        return db.scalar(
            select(HealthRuleVaccine).where(
                HealthRuleVaccine.health_rule_id
                == health_rule_id,
                HealthRuleVaccine.vaccine_id
                == vaccine_id,
            )
        )