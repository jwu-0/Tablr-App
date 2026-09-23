"""CORS. Owned by the backend, reviewed via CODEOWNERS.

The allowlist is explicit per environment. Never use "*": the app sends
a bearer token on every request, and a wildcard origin combined with
credentials is how that token ends up somewhere it should not be.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings

#: Origins always allowed outside production.
LOCAL_ORIGINS = [
    "http://localhost:8081",  # Expo web dev server
    "http://localhost:19006",  # legacy Expo web port
]


def allowed_origins(settings: Settings) -> list[str]:
    """Resolve the origin allowlist for this environment.

    Local development ports are added automatically everywhere except
    production, so nobody is tempted to widen the production list to
    make their laptop work.

    Raises:
        ValueError: if the configured list contains "*".
    """
    origins = list(settings.cors_origins)
    if not settings.is_production:
        origins.extend(o for o in LOCAL_ORIGINS if o not in origins)
    if "*" in origins:
        raise ValueError('CORS_ALLOWED_ORIGINS must not contain "*"')
    return origins


def configure_cors(app: FastAPI, settings: Settings) -> None:
    """Attach the CORS middleware to `app`.

    Only the headers the app actually sends are allowed through:
    `Authorization` for the Supabase JWT, `Content-Type` for JSON.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins(settings),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
