"""Report, block, strike, suspension, and appeal.

STUB: no database access yet. Built out after the core loop closes, but
the endpoints exist now so a report has somewhere to land on day one —
see "Trust and safety" in TABLR_PLAN.md.
"""

from app.deps import CurrentUser
from app.domains.trust_safety.schemas import (
    Appeal,
    Block,
    CreateAppealRequest,
    CreateBlockRequest,
    CreateReportRequest,
    Report,
    Suspension,
)


def create_report(user: CurrentUser, body: CreateReportRequest) -> Report:
    """Record a report and hand it to moderation."""
    # TODO: insert into reports, then notify the moderation queue.
    _ = user
    return Report(
        id="",
        subject_type=body.subject_type,
        subject_id=body.subject_id,
        reason=body.reason,
    )


def list_blocks(user: CurrentUser) -> list[Block]:
    """Return everybody the caller has blocked."""
    # TODO: select from blocks where blocker_id = user.id.
    _ = user
    return []


def create_block(user: CurrentUser, body: CreateBlockRequest) -> Block:
    """Block another student."""
    # TODO: insert into blocks. Blocking must hide content in both
    # directions, everywhere — discover, tables, and chat.
    _ = user
    return Block(blocked_id=body.blocked_id)


def remove_block(user: CurrentUser, blocked_id: str) -> None:
    """Unblock another student."""
    # TODO: delete from blocks.
    _ = (user, blocked_id)


def list_my_suspensions(user: CurrentUser) -> list[Suspension]:
    """Return the caller's active suspensions."""
    # TODO: select suspensions that have not ended or been lifted.
    _ = user
    return []


def create_appeal(user: CurrentUser, body: CreateAppealRequest) -> Appeal:
    """Challenge a suspension."""
    # TODO: insert into appeals, allowing one open appeal per
    # suspension.
    _ = user
    return Appeal(id="", suspension_id=body.suspension_id)
