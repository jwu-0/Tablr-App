"""Schemas for device registration."""

from pydantic import BaseModel, Field


class RegisterDeviceRequest(BaseModel):
    """Register a device for push.

    The app posts its Expo push token once the user grants permission.
    """

    expo_push_token: str = Field(min_length=10, max_length=200)
    platform: str = Field(pattern="^(ios|android|web)$")


class DeviceRegistration(BaseModel):
    """Acknowledgement that the token was stored."""

    registered: bool
