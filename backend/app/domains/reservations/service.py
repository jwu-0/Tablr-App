"""Reservation state machine.

The legal transitions live here, in one place, so that no router can
invent a new one. `TRANSITIONS` is the whole contract — read it before
changing behaviour.

STUB: no database access yet. Slice 8 fills these in — see
TABLR_PLAN.md.
"""

from functools import lru_cache

from app.config import Settings, get_settings
from app.core.errors import ConflictError, NotFoundError
from app.deps import CurrentUser
from app.domains.reservations.dispatch.base import ReservationDispatcher
from app.domains.reservations.dispatch.fake import (
    FakeReservationDispatcher,
)
from app.domains.reservations.dispatch.real import (
    RealReservationDispatcher,
)
from app.domains.reservations.schemas import (
    CreateReservationRequest,
    Reservation,
    ReservationStatus,
)

S = ReservationStatus

#: The only transitions the system permits. A status mapped to an empty
#: set is terminal.
TRANSITIONS: dict[ReservationStatus, frozenset[ReservationStatus]] = {
    S.PENDING: frozenset({S.DISPATCHED, S.CANCELLED}),
    S.DISPATCHED: frozenset({S.CONFIRMED, S.DECLINED, S.CANCELLED}),
    S.CONFIRMED: frozenset({S.SEATED, S.NO_SHOW, S.CANCELLED}),
    S.DECLINED: frozenset(),
    S.CANCELLED: frozenset(),
    S.SEATED: frozenset(),
    S.NO_SHOW: frozenset(),
}


def assert_transition(
    current: ReservationStatus, target: ReservationStatus
) -> None:
    """Check a status change against `TRANSITIONS`.

    Raises:
        ConflictError: if the move is not permitted.
    """
    if target not in TRANSITIONS[current]:
        raise ConflictError(
            f"Cannot move a reservation from {current} to {target}."
        )


@lru_cache
def get_dispatcher(
    settings: Settings | None = None,
) -> ReservationDispatcher:
    """Return the configured dispatcher, built once per settings."""
    settings = settings or get_settings()
    if settings.reservation_dispatch == "fake":
        return FakeReservationDispatcher()
    return RealReservationDispatcher(settings)


async def create_reservation(
    table_id: str, user: CurrentUser, body: CreateReservationRequest
) -> Reservation:
    """Finalise a full table and dispatch its reservation. Host only."""
    # TODO(slice-8): host only, table must be full; insert as pending,
    # dispatch, then record the resulting reservation_events row.
    _ = (user, body)
    raise NotFoundError(f"No table {table_id}.")


def get_reservation(table_id: str, user: CurrentUser) -> Reservation:
    """Return the reservation for a table. Members only."""
    _ = user
    raise NotFoundError(f"No reservation for table {table_id}.")


async def cancel_reservation(table_id: str, user: CurrentUser) -> Reservation:
    """Withdraw a reservation. Host only."""
    # TODO(slice-8): assert_transition, then dispatcher.cancel, then
    # record the event.
    _ = user
    raise NotFoundError(f"No reservation for table {table_id}.")
