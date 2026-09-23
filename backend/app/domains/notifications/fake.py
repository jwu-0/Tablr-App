"""Fake sender: logs instead of delivering.

Keeps every notification call site exercised in development without
needing device tokens or an Expo access token.
"""

import logging

from app.domains.notifications.base import (
    Notification,
    NotificationResult,
    NotificationSender,
)

logger = logging.getLogger(__name__)

CHANNEL = "fake"


class FakeNotificationSender(NotificationSender):
    """Writes the notification to the log and reports success."""

    async def send(self, notification: Notification) -> NotificationResult:
        """Log the notification and report every token as sent."""
        logger.info(
            "fake push -> %d recipient(s): %s / %s",
            len(notification.to_tokens),
            notification.title,
            notification.body,
        )
        return NotificationResult(
            sent=len(notification.to_tokens), failed=0, channel=CHANNEL
        )
