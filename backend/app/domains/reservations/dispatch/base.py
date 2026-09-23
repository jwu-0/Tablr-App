"""The reservation dispatch seam.

"Dispatch" is the act of getting a reservation in front of a
restaurant — today an email to a host, later a partner API. Everything
behind this interface is swappable.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class DispatchRequest:
    """What a dispatcher needs to place one reservation.

    Attributes:
        requested_for: Always UTC.
    """

    reservation_id: str
    restaurant_id: str
    party_size: int
    requested_for: datetime
    contact_name: str | None = None


@dataclass(frozen=True, slots=True)
class DispatchResult:
    """What came back.

    Attributes:
        channel: Which implementation handled it — fake, email, or
            partner_api. Persisted so a reservation can be reconciled
            later against the right system.
        reference: Provider-side identifier for that reconciliation.
    """

    accepted: bool
    channel: str
    reference: str | None = None
    reason: str | None = None


class ReservationDispatcher(ABC):
    """Send a reservation to a restaurant, and withdraw it again."""

    @abstractmethod
    async def dispatch(self, request: DispatchRequest) -> DispatchResult:
        """Send the reservation to the restaurant."""

    @abstractmethod
    async def cancel(self, *, reference: str) -> DispatchResult:
        """Withdraw a previously dispatched reservation."""
