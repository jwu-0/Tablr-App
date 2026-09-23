"""Verification endpoints.

Unverified users may browse; these are how they stop being unverified.
"""

from fastapi import APIRouter

from app.deps import CurrentUserDep, SettingsDep
from app.domains.verification import service
from app.domains.verification.base import VerificationStatus
from app.domains.verification.schemas import (
    ConfirmVerificationRequest,
    StartVerificationRequest,
    VerificationState,
)

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/start", response_model=VerificationState)
async def start(
    body: StartVerificationRequest,
    user: CurrentUserDep,
    settings: SettingsDep,
) -> VerificationState:
    """Begin verification for the given student email."""
    attempt = await service.get_provider(settings).start(
        user_id=user.id, email=str(body.email)
    )
    return VerificationState(**attempt.__dict__)


@router.post("/confirm", response_model=VerificationState)
async def confirm(
    body: ConfirmVerificationRequest, settings: SettingsDep
) -> VerificationState:
    """Complete verification using the token from the email."""
    attempt = await service.get_provider(settings).confirm(
        reference=body.reference, token=body.token
    )
    # TODO(slice-3): on VERIFIED, set profiles.is_verified and
    # verified_at.
    return VerificationState(**attempt.__dict__)


@router.get("/status", response_model=VerificationState)
async def status(user: CurrentUserDep) -> VerificationState:
    """Report where the caller's verification currently stands."""
    # TODO(slice-3): read profiles.is_verified.
    return VerificationState(
        status=VerificationStatus.VERIFIED
        if user.is_verified
        else VerificationStatus.UNSTARTED
    )
