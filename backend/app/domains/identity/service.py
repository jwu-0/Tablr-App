"""Identity logic: the Tablr account behind a Supabase auth user.

STUB: no database access yet. Slice 1 fills these in — see
TABLR_PLAN.md.
"""

from datetime import UTC, datetime

from app.deps import CurrentUser
from app.domains.identity.schemas import (
    AccountExport,
    DeleteAccountResult,
    Me,
)


def get_me(user: CurrentUser) -> Me:
    """Return the caller's own account record."""
    # TODO(slice-1): select from public.profiles where id = user.id.
    return Me(
        id=user.id,
        email=user.email or "unknown@example.edu",
        is_verified=user.is_verified,
    )


def export_account(user: CurrentUser) -> AccountExport:
    """Gather every row keyed to this user.

    Stubbed deliberately, but the endpoint exists from day one so the
    privacy obligation is visible in the API surface rather than
    remembered later.
    """
    # TODO: join across profiles, tables, chat, reservations, receipts,
    # and consent_records.
    return AccountExport(
        generated_at=datetime.now(UTC), profile={"id": user.id}
    )


def delete_account(user: CurrentUser) -> DeleteAccountResult:
    """Soft-delete the account now; purge it later.

    Soft delete keeps referential integrity for other people's tables
    and chat threads. The purge job removes PII once the retention
    window passes.
    """
    # TODO: set profiles.deleted_at, anonymise chat authorship, and
    # enqueue the purge.
    _ = user
    return DeleteAccountResult(scheduled=True, purge_after=None)
