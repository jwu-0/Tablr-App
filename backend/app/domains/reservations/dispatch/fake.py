"""Fake dispatcher: logs, then immediately accepts.

Lets the whole reservation state machine be exercised end to end with
no restaurant, no email provider, and no partner integration.
"""

import logging
import secrets

from app.domains.reservations.dispatch.base import (
    DispatchRequest,
    DispatchResult,
    ReservationDispatcher,
)

logger = logging.getLogger(__name__)

CHANNEL = "fake"


class FakeReservationDispatcher(ReservationDispatcher):
    """Accepts everything and records it in the log."""

    async def dispatch(self, request: DispatchRequest) -> DispatchResult:
        """Pretend to place the reservation, and always succeed."""
        reference = f"fake-{secrets.token_hex(6)}"
        logger.info(
            "fake dispatch: reservation=%s restaurant=%s party=%d "
            "for=%s ref=%s",
            request.reservation_id,
            request.restaurant_id,
            request.party_size,
            request.requested_for.isoformat(),
            reference,
        )
        return DispatchResult(
            accepted=True, channel=CHANNEL, reference=reference
        )

    async def cancel(self, *, reference: str) -> DispatchResult:
        """Pretend to withdraw the reservation, and always succeed."""
        logger.info("fake dispatch cancelled: ref=%s", reference)
        return DispatchResult(
            accepted=True, channel=CHANNEL, reference=reference
        )
