"""Schemas for the reservation lifecycle."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ReservationStatus(StrEnum):
    """Every state a reservation can occupy.

    Legal moves between them live in `service.TRANSITIONS`.
    """

    PENDING = "pending"
    DISPATCHED = "dispatched"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    SEATED = "seated"
    NO_SHOW = "no_show"


class Reservation(BaseModel):
    """A booking for one table.

    Attributes:
        requested_for: Always UTC.
        dispatch_channel: Which dispatcher handled it, for later
            reconciliation.
    """

    id: str
    table_id: str
    restaurant_id: str
    party_size: int = Field(ge=1, le=12)
    requested_for: datetime
    status: ReservationStatus = ReservationStatus.PENDING
    dispatch_channel: str | None = None


class CreateReservationRequest(BaseModel):
    """Finalise a table and book it.

    Party size is derived from the table's members rather than sent by
    the client, so it cannot disagree with who actually has a seat.
    `requested_for` defaults to the table's scheduled time.
    """

    requested_for: datetime | None = None


class ReservationEvent(BaseModel):
    """One recorded transition, kept for debugging and disputes."""

    from_status: ReservationStatus | None = None
    to_status: ReservationStatus
    created_at: datetime
