"""Verification logic.

Picks the provider from config so no caller ever chooses one.
"""

from functools import lru_cache

from app.config import Settings, get_settings
from app.domains.verification.base import VerificationProvider
from app.domains.verification.fake import FakeVerificationProvider
from app.domains.verification.provider import RealVerificationProvider


@lru_cache
def get_provider(
    settings: Settings | None = None,
) -> VerificationProvider:
    """Return the configured provider, built once per settings."""
    settings = settings or get_settings()
    if settings.verification_provider == "fake":
        return FakeVerificationProvider(settings)
    return RealVerificationProvider(settings)
