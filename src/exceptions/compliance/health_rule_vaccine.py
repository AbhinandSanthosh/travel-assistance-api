from src.exceptions.base import AppException


class HealthRuleVaccineAlreadyExistsError(
    AppException,
):
    """Raised when a health rule vaccine already exists."""

    def __init__(
        self,
        health_rule_id: int,
        vaccine_id: int,
    ) -> None:
        self.health_rule_id = health_rule_id
        self.vaccine_id = vaccine_id

        super().__init__(
            "Health Rule Vaccine already exists "
            f"for health_rule_id '{health_rule_id}' "
            f"and vaccine_id '{vaccine_id}'."
        )


class HealthRuleVaccineNotFoundError(
    AppException,
):
    """Raised when a health rule vaccine cannot be found."""

    def __init__(
        self,
        health_rule_vaccine_id: int,
    ) -> None:
        self.health_rule_vaccine_id = (
            health_rule_vaccine_id
        )

        super().__init__(
            "Health Rule Vaccine with id "
            f"{health_rule_vaccine_id} "
            "was not found."
        )