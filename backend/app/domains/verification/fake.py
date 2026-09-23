"""Fake verifier: a domain allowlist plus an email confirmation loop.

Good enough for the whole beta. Anyone whose email domain appears in
`VERIFICATION_ALLOWLIST_DOMAINS` is approved once they click the link.
"""

import secrets

from app.config import Settings
from app.domains.verification.base import (
    VerificationAttempt,
    VerificationProvider,
    VerificationStatus,
)


class FakeVerificationProvider(VerificationProvider):
    """Approves allowlisted domains after a token round-trip."""

    def __init__(self, settings: Settings) -> None:
        """Capture the allowlist and start an empty pending map."""
        self._allowlist = settings.allowlisted_email_domains
        # TODO(slice-3): move this out of process memory so pending
        # attempts survive a restart.
        self._pending: dict[str, str] = {}

    async def start(self, *, user_id: str, email: str) -> VerificationAttempt:
        """Issue a token for an allowlisted domain, or reject."""
        domain = email.rsplit("@", 1)[-1].lower()
        if domain not in self._allowlist:
            return VerificationAttempt(
                status=VerificationStatus.REJECTED,
                reason=f"{domain} is not a recognised student domain.",
            )

        reference = secrets.token_urlsafe(16)
        self._pending[reference] = secrets.token_urlsafe(16)
        # TODO(slice-3): send the confirmation email.
        _ = user_id
        return VerificationAttempt(
            status=VerificationStatus.PENDING, reference=reference
        )

    async def confirm(
        self, *, reference: str, token: str
    ) -> VerificationAttempt:
        """Verify the token against the one issued by `start`."""
        expected = self._pending.get(reference)
        if expected is None:
            return VerificationAttempt(
                status=VerificationStatus.REJECTED,
                reason="Unknown reference.",
            )
        if not secrets.compare_digest(expected, token):
            return VerificationAttempt(
                status=VerificationStatus.PENDING,
                reference=reference,
                reason="Token did not match.",
            )
        del self._pending[reference]
        return VerificationAttempt(
            status=VerificationStatus.VERIFIED, reference=reference
        )
