"""Trust and safety endpoints.

These are available to unverified users too: being unable to prove you
are a student must never stop you reporting somebody.
"""

from fastapi import APIRouter, status

from app.deps import CurrentUserDep
from app.domains.trust_safety import service
from app.domains.trust_safety.schemas import (
    Appeal,
    Block,
    CreateAppealRequest,
    CreateBlockRequest,
    CreateReportRequest,
    Report,
    Suspension,
)

router = APIRouter(tags=["trust-safety"])


@router.post("/reports", response_model=Report, status_code=201)
async def create_report(
    body: CreateReportRequest, user: CurrentUserDep
) -> Report:
    """Flag a profile, table, or message for moderation."""
    return service.create_report(user, body)


@router.get("/blocks", response_model=list[Block])
async def list_blocks(user: CurrentUserDep) -> list[Block]:
    """Return everybody the caller has blocked."""
    return service.list_blocks(user)


@router.post("/blocks", response_model=Block, status_code=201)
async def create_block(
    body: CreateBlockRequest, user: CurrentUserDep
) -> Block:
    """Block another student."""
    return service.create_block(user, body)


@router.delete("/blocks/{blocked_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_block(blocked_id: str, user: CurrentUserDep) -> None:
    """Unblock another student."""
    service.remove_block(user, blocked_id)


@router.get("/me/suspensions", response_model=list[Suspension])
async def list_my_suspensions(user: CurrentUserDep) -> list[Suspension]:
    """Return the caller's active suspensions."""
    return service.list_my_suspensions(user)


@router.post("/appeals", response_model=Appeal, status_code=201)
async def create_appeal(
    body: CreateAppealRequest, user: CurrentUserDep
) -> Appeal:
    """Challenge a suspension."""
    return service.create_appeal(user, body)
