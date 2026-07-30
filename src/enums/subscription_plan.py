from enum import Enum


class SubscriptionPlan(str, Enum):
    """Supported subscription plans."""

    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"