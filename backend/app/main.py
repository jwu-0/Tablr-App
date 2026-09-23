"""Tablr API.

Builds the app, mounts every domain router, and configures CORS and
error handling. All business logic lives in `app/domains/*/service.py`;
this module only wires things together.
"""

import logging

from fastapi import FastAPI

from app.config import Settings, get_settings
from app.core.cors import configure_cors
from app.core.errors import configure_error_handlers
from app.domains.chat.router import router as chat_router
from app.domains.identity.router import router as identity_router
from app.domains.matching.router import router as matching_router
from app.domains.notifications.router import router as notifications_router
from app.domains.profiles.router import router as profiles_router
from app.domains.receipts.router import router as receipts_router
from app.domains.reservations.router import router as reservations_router
from app.domains.restaurants.router import router as restaurants_router
from app.domains.tables.router import router as tables_router
from app.domains.trust_safety.router import router as trust_safety_router
from app.domains.verification.router import router as verification_router

API_PREFIX = "/v1"

# Order matters only for documentation grouping.
DOMAIN_ROUTERS = (
    identity_router,
    verification_router,
    profiles_router,
    restaurants_router,
    matching_router,
    tables_router,
    chat_router,
    reservations_router,
    receipts_router,
    trust_safety_router,
    notifications_router,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a configured FastAPI application.

    Taking `settings` as an argument (rather than reading the global)
    keeps tests able to build an app with a different environment
    without touching the settings cache.
    """
    settings = settings or get_settings()
    logging.basicConfig(level=settings.log_level.upper())

    app = FastAPI(
        title="Tablr API",
        version="0.1.0",
        description=(
            "The only seam between the Expo app and Tablr's data. "
            "The app never talks to Postgres directly."
        ),
        openapi_url="/openapi.json",
        docs_url="/docs",
    )

    configure_cors(app, settings)
    configure_error_handlers(app)

    for router in DOMAIN_ROUTERS:
        app.include_router(router, prefix=API_PREFIX)

    @app.get("/health", tags=["meta"], summary="Liveness probe")
    async def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    return app


app = create_app()
