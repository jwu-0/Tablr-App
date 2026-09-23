"""Receipt confirmation.

STUB: no database access yet. Slice 9 fills these in — see
TABLR_PLAN.md.
"""

from functools import lru_cache

from app.config import Settings, get_settings
from app.core.errors import NotFoundError
from app.deps import CurrentUser
from app.domains.receipts.schemas import Receipt, SubmitReceiptRequest
from app.domains.receipts.verify.base import ReceiptVerifier
from app.domains.receipts.verify.fake import FakeReceiptVerifier
from app.domains.receipts.verify.real import RealReceiptVerifier


@lru_cache
def get_verifier(settings: Settings | None = None) -> ReceiptVerifier:
    """Return the configured verifier, built once per settings."""
    settings = settings or get_settings()
    if settings.receipt_verifier == "fake":
        return FakeReceiptVerifier()
    return RealReceiptVerifier(settings)


async def submit_receipt(
    table_id: str, user: CurrentUser, body: SubmitReceiptRequest
) -> Receipt:
    """Submit a receipt and run it past the verifier. Members only."""
    # TODO(slice-9): insert into receipts, run the verifier, and on
    # VERIFIED mark the table completed.
    _ = (user, body)
    raise NotFoundError(f"No table {table_id}.")


def get_receipt(table_id: str, user: CurrentUser) -> Receipt:
    """Return the receipt for a table. Members only."""
    _ = user
    raise NotFoundError(f"No receipt for table {table_id}.")
