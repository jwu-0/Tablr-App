"""Shared FastAPI dependencies.

Authorization happens here and in the domain services — never in a
router body. `get_current_user` answers "who is this?";
`require_verified` answers "are they allowed to act?"; the
per-resource checks ("may they touch *this* table?") live in each
domain's service.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.core.errors import NotVerifiedError
from app.core.security import InvalidTokenError, decode_supabase_jwt

#: `auto_error=False` so a missing header reaches our own handler and
#: produces the standard error envelope rather than FastAPI's default.
bearer_scheme = HTTPBearer(auto_error=False)

SettingsDep = Annotated[Settings, Depends(get_settings)]


class CurrentUser(BaseModel):
    """The authenticated caller, as the rest of the backend sees them.

    Deliberately small: it holds what authorization needs and nothing
    else. Anything richer belongs in the profiles domain.
    """

    id: str
    email: str | None = None
    #: STUB: always False until slice 1 reads `profiles.is_verified`.
    is_verified: bool = False


async def get_current_user(
    settings: SettingsDep,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ] = None,
) -> CurrentUser:
    """Verify the Supabase JWT and return the caller.

    Raises:
        HTTPException: 401 when the token is absent or untrustworthy.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        claims = decode_supabase_jwt(credentials.credentials, settings)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # TODO(slice-1): read profiles.is_verified rather than defaulting.
    return CurrentUser(id=claims.user_id, email=claims.email)


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]


async def require_verified(user: CurrentUserDep) -> CurrentUser:
    """Gate for acting, as opposed to browsing.

    Unverified students may read Discover. They may not join a table,
    send a chat message, or reserve. Attach this to every such endpoint.

    Raises:
        NotVerifiedError: 403 with the `not_verified` code, which the
            app handles by routing to the verification screen.
    """
    if not user.is_verified:
        raise NotVerifiedError()
    return user


VerifiedUserDep = Annotated[CurrentUser, Depends(require_verified)]
