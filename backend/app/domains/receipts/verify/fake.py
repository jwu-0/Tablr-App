"""Fake verifier: accepts anything with a positive total.

Enough to exercise the closing step of the loop without OCR or a human
review queue.
"""

import logging

from app.domains.receipts.verify.base import (
    ReceiptStatus,
    ReceiptSubmission,
    ReceiptVerdict,
    ReceiptVerifier,
)

logger = logging.getLogger(__name__)

CHANNEL = "fake"


class FakeReceiptVerifier(ReceiptVerifier):
    """Approves any receipt that names a positive amount."""

    async def verify(self, submission: ReceiptSubmission) -> ReceiptVerdict:
        """Accept a positive total; reject anything else."""
        logger.info(
            "fake receipt verify: receipt=%s table=%s total_cents=%s",
            submission.receipt_id,
            submission.table_id,
            submission.total_cents,
        )
        if submission.total_cents is None or submission.total_cents <= 0:
            return ReceiptVerdict(
                status=ReceiptStatus.REJECTED,
                channel=CHANNEL,
                reason="Receipt total must be a positive amount in cents.",
            )
        return ReceiptVerdict(
            status=ReceiptStatus.VERIFIED,
            channel=CHANNEL,
            extracted_total_cents=submission.total_cents,
        )
