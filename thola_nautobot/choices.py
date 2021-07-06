"""Choicesets for thola nautobot."""
from nautobot.utilities.choices import ChoiceSet


class TholaOnboardingStatusChoice(ChoiceSet):
    """Valid values for TholaOnboarding "status"."""

    STATUS_UNKNOWN = "unknown"
    STATUS_SUCCESS = "success"
    STATUS_RUNNING = "running"
    STATUS_PENDING = "pending"
    STATUS_FAILED = "failed"

    CHOICES = (
        (STATUS_UNKNOWN, "unknown"),
        (STATUS_SUCCESS, "success"),
        (STATUS_RUNNING, "running"),
        (STATUS_PENDING, "pending"),
        (STATUS_FAILED, "failed"),
    )
