"""Error types and the handlers that turn them into responses.

Every error the client sees has the same shape::

    {"error": {"code": "not_found", "message": "..."}}

so the typed client can branch on `code` rather than parsing prose.
Add a subclass here rather than raising `HTTPException` in a service —
the code is part of the contract, and prose is not.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class TablrError(Exception):
    """Base class for errors that map cleanly onto a status code.

    Subclasses set `status_code` and `code`. The default message is the
    subclass docstring, so a raise with no arguments still reads well to
    a user.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_error"

    def __init__(self, message: str | None = None) -> None:
        """Build the error, defaulting the message to the docstring."""
        default = self.__class__.__doc__ or "Something went wrong."
        self.message = message or default
        super().__init__(self.message)


class NotFoundError(TablrError):
    """The requested resource does not exist."""

    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class PermissionDeniedError(TablrError):
    """You are not allowed to do that."""

    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"


class NotVerifiedError(TablrError):
    """Verify your student status before you join, chat, or reserve."""

    status_code = status.HTTP_403_FORBIDDEN
    code = "not_verified"


class ConflictError(TablrError):
    """That conflicts with the current state of the resource."""

    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class NotImplementedYetError(TablrError):
    """Scaffolded but not built yet."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED
    code = "not_implemented"


def configure_error_handlers(app: FastAPI) -> None:
    """Register the handler that renders `TablrError` as JSON."""

    @app.exception_handler(TablrError)
    async def handle_tablr_error(_: Request, exc: TablrError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )
