"""Device registration endpoints."""

from fastapi import APIRouter

from app.deps import CurrentUserDep
from app.domains.notifications import service
from app.domains.notifications.schemas import (
    DeviceRegistration,
    RegisterDeviceRequest,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/devices", response_model=DeviceRegistration, status_code=201)
async def register_device(
    body: RegisterDeviceRequest, user: CurrentUserDep
) -> DeviceRegistration:
    """Store this device's push token against the caller."""
    return service.register_device(user, body)
