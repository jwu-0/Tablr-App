"""Supabase JWT verification.

The app authenticates against Supabase and sends the resulting access
token as `Authorization: Bearer <jwt>`. This module turns that token
into a trusted identity, and is the only place that decides who
somebody is.

STUB: in non-production environments with no `SUPABASE_JWT_SECRET`, the
token is decoded *without* verifying its signature, so the stack runs
with no Supabase project at all. Production refuses to start down that
path. Slice 1 removes the fallback — see TABLR_PLAN.md.
"""

from dataclasses import dataclass
from typing import Any

from jose import JWTError, jwt

from app.config import Settings


@dataclass(frozen=True, slots=True)
class TokenClaims:
    """The subset of the Supabase JWT the backend trusts.

    Attributes:
        user_id: The `sub` claim — the Supabase auth user id, and the
            primary key of `public.profiles`.
        email: The `email` claim, when present.
        raw: The full payload, for callers needing a claim that is
            not promoted above. Prefer adding a field to reaching in.
    """

    user_id: str
    email: str | None
    raw: dict[str, Any]


class InvalidTokenError(Exception):
    """The bearer token was missing, malformed, or unverifiable."""


def decode_supabase_jwt(token: str, settings: Settings) -> TokenClaims:
    """Verify `token` and return its claims.

    Raises:
        InvalidTokenError: if the token cannot be trusted.
        RuntimeError: in production, if no JWT secret is configured.
    """
    if not settings.supabase_jwt_secret:
        if settings.is_production:
            raise RuntimeError(
                "SUPABASE_JWT_SECRET is required in production."
            )
        # Local development without a Supabase project.
        # TODO(slice-1): remove once local Supabase is the default.
        return _decode_unverified(token)

    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError as exc:
        raise InvalidTokenError(str(exc)) from exc

    return _claims_from_payload(payload)


def _decode_unverified(token: str) -> TokenClaims:
    """Read claims without checking the signature.

    Never reachable in production.
    """
    try:
        payload = jwt.get_unverified_claims(token)
    except JWTError as exc:
        raise InvalidTokenError(str(exc)) from exc
    return _claims_from_payload(payload)


def _claims_from_payload(payload: dict[str, Any]) -> TokenClaims:
    """Project a decoded payload onto `TokenClaims`."""
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("token has no subject")
    return TokenClaims(
        user_id=user_id, email=payload.get("email"), raw=payload
    )
