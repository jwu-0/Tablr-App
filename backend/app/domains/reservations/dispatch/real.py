"""Real dispatcher: transactional email first, then a partner API.

STUB: not wired. Flip `RESERVATION_DISPATCH` once there is a real
channel — see "Real providers" in TABLR_PLAN.md.
"""

from app.config import Settings
from app.core.errors import NotImplementedYetError
from app.domains.reservations.dispatch.base import (
    DispatchRequest,
    DispatchResult,
    ReservationDispatcher,
)


class RealReservationDispatcher(ReservationDispatcher):
    """Places reservations for real. Every method raises for now."""

    def __init__(self, settings: Settings) -> None:
        """Capture the transactional email credentials."""
        self._email_api_key = settings.transactional_email_api_key

    async def dispatch(self, request: DispatchRequest) -> DispatchResult:
        """Send the reservation to the restaurant. Not implemented."""
        raise NotImplementedYetError(
            "Real reservation dispatch is not wired yet."
        )

    async def cancel(self, *, reference: str) -> DispatchResult:
        """Withdraw the reservation. Not implemented."""
        raise NotImplementedYetError(
            "Real reservation dispatch is not wired yet."
        )
