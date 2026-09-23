"""Profile logic.

STUB: no database access yet. Slice 2 fills these in — see
TABLR_PLAN.md.
"""

from app.deps import CurrentUser
from app.domains.profiles.schemas import (
    CreateTagRequest,
    InterestTag,
    PublicProfile,
    TagRequest,
    UpdateProfileRequest,
)


def get_profile(profile_id: str) -> PublicProfile:
    """Return another student's public profile."""
    # TODO(slice-2): select from profiles + profile_interest_tags, and
    # derive age from date_of_birth.
    return PublicProfile(id=profile_id)


def update_my_profile(
    user: CurrentUser, body: UpdateProfileRequest
) -> PublicProfile:
    """Apply a partial update to the caller's own profile."""
    # TODO(slice-2): update profiles, and replace profile_interest_tags
    # atomically when tag_ids is present.
    _ = body
    return PublicProfile(id=user.id)


def list_tags() -> list[InterestTag]:
    """Return the canonical tag list users pick from."""
    # TODO(slice-2): select from interest_tags where deleted_at is null.
    return []


def request_tag(user: CurrentUser, body: CreateTagRequest) -> TagRequest:
    """Record a request for a tag that does not exist yet."""
    # TODO(slice-2): insert into interest_tag_requests as 'pending'.
    _ = user
    return TagRequest(id="", raw_text=body.raw_text, status="pending")
