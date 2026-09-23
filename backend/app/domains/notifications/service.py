"""Notification dispatch. Picks the sender from config."""

from functools import lru_cache

from app.config import Settings, get_settings
from app.deps import CurrentUser
from app.domains.notifications.base import NotificationSender
from app.domains.notifications.fake import FakeNotificationSender
from app.domains.notifications.push import ExpoPushNotificationSender
from app.domains.notifications.schemas import (
    DeviceRegistration,
    RegisterDeviceRequest,
)


@lru_cache
def get_sender(settings: Settings | None = None) -> NotificationSender:
    """Return the configured sender, built once per settings."""
    settings = settings or get_settings()
    if settings.notification_provider == "fake":
        return FakeNotificationSender()
    return ExpoPushNotificationSender(settings)


def register_device(
    user: CurrentUser, body: RegisterDeviceRequest
) -> DeviceRegistration:
    """Store a device's push token against the caller."""
    # TODO: upsert (profile_id, expo_push_token, platform) into a
    # devices table, which does not exist yet.
    _ = (user, body)
    return DeviceRegistration(registered=True)
