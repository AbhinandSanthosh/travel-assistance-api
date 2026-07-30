from enum import Enum


class SimulationStatus(str, Enum):
    """Supported simulation statuses."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"