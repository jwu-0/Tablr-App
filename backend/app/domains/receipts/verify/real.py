"""Real receipt verification: OCR, or a human review queue.

STUB: not wired. Flip `RECEIPT_VERIFIER` when there is something to
flip to — see "Real providers" in TABLR_PLAN.md.
"""

from app.config import Settings
from app.core.errors import NotImplementedYetError
from app.domains.receipts.verify.base import (
    ReceiptSubmission,
    ReceiptVerdict,
    ReceiptVerifier,
)


class RealReceiptVerifier(ReceiptVerifier):
    """Verifies receipts for real. Raises for now."""

    def __init__(self, settings: Settings) -> None:
        """Capture settings for the eventual OCR or queue client."""
        self._settings = settings

    async def verify(self, submission: ReceiptSubmission) -> ReceiptVerdict:
        """Rule on a receipt. Not implemented."""
        raise NotImplementedYetError(
            "Real receipt verification is not wired yet."
        )
