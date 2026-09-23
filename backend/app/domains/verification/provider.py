"""Real verification provider.

STUB: not wired. Flip `VERIFICATION_PROVIDER` once a contract exists
and implement against the vendor's API using `VERIFICATION_API_KEY`.
See "Real providers" in TABLR_PLAN.md.
"""

from app.config import Settings
from app.core.errors import NotImplementedYetError
from app.domains.verification.base import (
    VerificationAttempt,
    VerificationProvider,
)


class RealVerificationProvider(VerificationProvider):
    """Third-party student verification. Every method raises for now."""

    def __init__(self, settings: Settings) -> None:
        """Capture the vendor API key."""
        self._api_key = settings.verification_api_key

    async def start(self, *, user_id: str, email: str) -> VerificationAttempt:
        """Begin verification with the vendor. Not implemented."""
        raise NotImplementedYetError(
            "Real student verification is not wired yet."
        )

    async def confirm(
        self, *, reference: str, token: str
    ) -> VerificationAttempt:
        """Complete verification with the vendor. Not implemented."""
        raise NotImplementedYetError(
            "Real student verification is not wired yet."
        )
