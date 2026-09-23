"""The receipt verification seam.

Confirming a receipt is what closes the loop: proof the group actually
showed up and ate. Today a fake or a human decides; later it might be
OCR.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class ReceiptStatus(StrEnum):
    """Where a submitted receipt stands."""

    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class ReceiptSubmission:
    """What a verifier is given.

    Attributes:
        total_cents: Integer minor units, never a float.
    """

    receipt_id: str
    table_id: str
    image_path: str | None
    total_cents: int | None


@dataclass(frozen=True, slots=True)
class ReceiptVerdict:
    """What the verifier decided.

    Attributes:
        channel: Which implementation ruled — fake, ocr, or manual.
        extracted_total_cents: What the verifier read off the receipt,
            when it can read. Integer minor units.
    """

    status: ReceiptStatus
    channel: str
    reason: str | None = None
    extracted_total_cents: int | None = None


class ReceiptVerifier(ABC):
    """Rule on submitted receipts."""

    @abstractmethod
    async def verify(self, submission: ReceiptSubmission) -> ReceiptVerdict:
        """Rule on one submitted receipt."""
