"""Account endpoints.

Includes the two privacy endpoints (`GET /me/export` and `DELETE /me`)
that exist from day one, so the obligation is visible in the contract
rather than deferred.
"""

from fastapi import APIRouter

from app.deps import CurrentUserDep
from app.domains.identity import service
from app.domains.identity.schemas import (
    AccountExport,
    DeleteAccountResult,
    Me,
)

router = APIRouter(prefix="/me", tags=["identity"])


@router.get("", response_model=Me, summary="Get the signed-in account")
async def read_me(user: CurrentUserDep) -> Me:
    """Return the caller's own account record."""
    return service.get_me(user)


@router.get("/export", response_model=AccountExport, summary="Export my data")
async def export_me(user: CurrentUserDep) -> AccountExport:
    """Return everything Tablr holds about the caller."""
    return service.export_account(user)


@router.delete("", response_model=DeleteAccountResult, summary="Delete me")
async def delete_me(user: CurrentUserDep) -> DeleteAccountResult:
    """Soft-delete the caller's account and schedule the purge."""
    return service.delete_account(user)
