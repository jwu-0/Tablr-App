"""Profile and interest-taxonomy schemas."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class TagCategory(StrEnum):
    """Which axis of a person a tag describes."""

    CUISINE = "cuisine"
    DIET = "diet"
    VIBE = "vibe"
    COMMUNITY = "community"
    ACTIVITY = "activity"


class InterestTag(BaseModel):
    """A canonical preset tag.

    Users pick from these; they cannot invent them. See `TagRequest`
    for the free-text path.
    """

    id: str
    slug: str
    label: str
    category: TagCategory


class TagRequest(BaseModel):
    """Free text a user wanted as a tag, awaiting review.

    Keeping free text out of the tag table is what stops the taxonomy
    fragmenting into 40 spellings of "boba" and quietly breaking match
    scoring.
    """

    id: str
    raw_text: str
    status: str
    mapped_tag_id: str | None = None


class CreateTagRequest(BaseModel):
    """Ask for a tag that does not exist yet."""

    raw_text: str = Field(min_length=2, max_length=40)


class PublicProfile(BaseModel):
    """What another student sees.

    Never includes the email address or the date of birth — only the
    age derived from it.
    """

    id: str
    display_name: str | None = None
    age: int | None = None
    bio: str | None = None
    avatar_url: str | None = None
    is_verified: bool = False
    tags: list[InterestTag] = []


class UpdateProfileRequest(BaseModel):
    """Partial update of the caller's own profile.

    `tag_ids` replaces the whole tag set when present, and leaves it
    untouched when omitted.
    """

    display_name: str | None = Field(default=None, min_length=1, max_length=50)
    date_of_birth: date | None = None
    bio: str | None = Field(default=None, max_length=280)
    avatar_url: str | None = None
    tag_ids: list[str] | None = None
