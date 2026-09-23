"""Expo Push.

STUB: not wired. Flip `NOTIFICATION_PROVIDER=expo_push` and implement
against the Expo push API using `EXPO_ACCESS_TOKEN`. See "Real
providers" in TABLR_PLAN.md and
https://docs.expo.dev/push-notifications/sending-notifications/
"""

from app.config import Settings
from app.core.errors import NotImplementedYetError
from app.domains.notifications.base import (
    Notification,
    NotificationResult,
    NotificationSender,
)

EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"

CHANNEL = "expo_push"


class ExpoPushNotificationSender(NotificationSender):
    """Delivers through Expo Push. Raises for now."""

    def __init__(self, settings: Settings) -> None:
        """Capture the Expo access token."""
        self._access_token = settings.expo_access_token

    async def send(self, notification: Notification) -> NotificationResult:
        """Deliver through Expo Push. Not implemented."""
        raise NotImplementedYetError("Expo Push is not wired yet.")
