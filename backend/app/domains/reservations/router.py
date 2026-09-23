"""Reservation endpoints, scoped to a table."""

from fastapi import APIRouter

from app.deps import CurrentUserDep, VerifiedUserDep
from app.domains.reservations import service
from app.domains.reservations.schemas import (
    CreateReservationRequest,
    Reservation,
)

router = APIRouter(
    prefix="/tables/{table_id}/reservation", tags=["reservations"]
)


@router.get("", response_model=Reservation)
async def get_reservation(table_id: str, user: CurrentUserDep) -> Reservation:
    """Return this table's reservation. Members only."""
    return service.get_reservation(table_id, user)


@router.post("", response_model=Reservation, status_code=201)
async def create_reservation(
    table_id: str, body: CreateReservationRequest, user: VerifiedUserDep
) -> Reservation:
    """Finalise the table and book it. Host only."""
    return await service.create_reservation(table_id, user, body)


@router.delete("", response_model=Reservation)
async def cancel_reservation(
    table_id: str, user: VerifiedUserDep
) -> Reservation:
    """Withdraw this table's reservation. Host only."""
    return await service.cancel_reservation(table_id, user)
