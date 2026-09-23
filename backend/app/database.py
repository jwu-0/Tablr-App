"""Postgres access.

Connects with the Supabase **service role**, which bypasses row-level
security. That is deliberate: the backend is the single door and does
its own authorization in `deps.py`. This module must never be importable
from the Expo app.

STUB: the engine is created lazily and nothing uses a session yet.
Slice 1 introduces the first real query — see TABLR_PLAN.md.
"""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    """Build the connection pool, once per process.

    Raises:
        RuntimeError: if `DATABASE_URL` is unset. Failing here beats
            failing halfway through a request with a vaguer error.
    """
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is unset. Copy backend/.env.example to backend/.env."
        )
    return create_engine(
        settings.database_url, pool_pre_ping=True, future=True
    )


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    """Return the shared session factory bound to the engine."""
    return sessionmaker(
        bind=get_engine(), autoflush=False, expire_on_commit=False
    )


def get_db() -> Iterator[Session]:
    """Yield a request-scoped session, as a FastAPI dependency.

    The session closes when the request ends. Services take the session
    as an argument rather than reaching for a global.
    """
    with get_session_factory()() as session:
        yield session
