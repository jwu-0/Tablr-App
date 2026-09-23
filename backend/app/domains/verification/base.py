"""The verification seam.

Student verification is a buyable service (SheerID and friends).
Everything behind this interface is swappable, so the rest of the
backend never learns which provider — or fake — is in play.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class VerificationStatus(StrEnum):
    """Where a verification attempt has got to."""

    UNSTARTED = "unstarted"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class VerificationAttempt:
    """The outcome of one call to a provider.

    Attributes:
        status: Where the attempt now stands.
        reference: Provider-side identifier, echoed back on confirm.
        reason: Human-readable explanation when rejected or stalled.
    """

    status: VerificationStatus
    reference: str | None = None
    reason: str | None = None


class VerificationProvider(ABC):
    """Start a verification, then confirm it."""

    @abstractmethod
    async def start(self, *, user_id: str, email: str) -> VerificationAttempt:
        """Begin verification for `email`."""

    @abstractmethod
    async def confirm(
        self, *, reference: str, token: str
    ) -> VerificationAttempt:
        """Complete verification using the emailed token."""
