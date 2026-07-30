from src.exceptions.base import AppException


class RuleSimulationNotFoundError(AppException):
    """Raised when a rule simulation cannot be found."""

    def __init__(
        self,
        simulation_id: int,
    ):
        self.simulation_id = simulation_id

        super().__init__(
            f"Rule simulation with id {simulation_id} was not found."
        )