"""Matching orchestration.

Loads rows, projects them into `MatchInput`, calls the pure scorers,
and ranks. Every impure concern lives here so `scoring.py` stays
testable in isolation.

STUB: no database access yet. Slice 5 fills this in — see
TABLR_PLAN.md.
"""

from app.deps import CurrentUser
from app.domains.matching.schemas import MatchPreview


def preview_matches(user: CurrentUser, limit: int = 20) -> MatchPreview:
    """Return the caller's top candidates, highest score first."""
    # TODO(slice-5): load candidate profiles, project each to
    # MatchInput, score_pair against the caller, sort desc, take limit.
    _ = (user, limit)
    return MatchPreview()
