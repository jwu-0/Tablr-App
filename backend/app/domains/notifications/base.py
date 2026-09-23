"""The notification seam."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Notification:
    """One push, addressed to one or more devices.

    Attributes:
        to_tokens: Expo push tokens, e.g. "ExponentPushToken[...]".
        data: Payload the app reads to deep-link on tap. Keep it small
            and non-sensitive — push payloads are not private.
    """

    to_tokens: tuple[str, ...]
    title: str
    body: str
    data: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NotificationResult:
    """How delivery went."""

    sent: int
    failed: int
    channel: str


class NotificationSender(ABC):
    """Deliver push notifications."""

    @abstractmethod
    async def send(self, notification: Notification) -> NotificationResult:
        """Deliver a push notification."""
