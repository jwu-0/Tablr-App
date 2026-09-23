"""Configuration.

Every secret enters the process here and nowhere else. Values come from
the environment (or `backend/.env` locally). See `.env.example` for the
full list — it documents every name, with no values.
"""

from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Where this process is running.

    Some behaviour is deliberately laxer outside production — see
    `core.security.decode_supabase_jwt` and `core.cors.allowed_origins`.
    """

    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Every environment variable the backend reads.

    Defaults are safe for local development: no credentials, and the
    fake provider selected for each swappable service.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    environment: Environment = Environment.LOCAL
    log_level: str = "info"

    # --- Supabase -----------------------------------------------------
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""
    supabase_jwks_url: str = ""

    # --- Database -----------------------------------------------------
    database_url: str = ""

    # --- CORS: explicit allowlist, never "*" --------------------------
    cors_allowed_origins: str = "http://localhost:8081,http://localhost:19006"

    # --- Provider selection -------------------------------------------
    # Fakes stay wired until there is a real contract to flip to.
    verification_provider: str = "fake"
    reservation_dispatch: str = "fake"
    receipt_verifier: str = "fake"
    notification_provider: str = "fake"

    # --- Third-party credentials --------------------------------------
    # All unset while the fakes are in use.
    verification_api_key: str = ""
    transactional_email_api_key: str = ""
    maps_api_key: str = ""
    moderation_api_key: str = ""
    error_monitoring_dsn: str = ""
    expo_access_token: str = ""

    # --- Fake verification --------------------------------------------
    verification_allowlist_domains: str = "example.edu"

    @property
    def cors_origins(self) -> list[str]:
        """Parse `CORS_ALLOWED_ORIGINS` into a list of origins."""
        raw = self.cors_allowed_origins.split(",")
        return [o.strip() for o in raw if o.strip()]

    @property
    def allowlisted_email_domains(self) -> set[str]:
        """Domains the fake verifier auto-approves, lower-cased."""
        return {
            d.strip().lower()
            for d in self.verification_allowlist_domains.split(",")
            if d.strip()
        }

    @property
    def is_production(self) -> bool:
        """True in production, where local shortcuts are refused."""
        return self.environment is Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    """Read the settings from the environment, once per process.

    Cached so every FastAPI dependency shares one instance. A test
    needing different values should build `Settings` directly rather
    than clearing this cache.
    """
    return Settings()
