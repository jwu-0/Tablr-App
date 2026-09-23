"""Schemas for the matching endpoints."""

from pydantic import BaseModel, Field


class MatchCandidate(BaseModel):
    """One ranked person, with the score that ranked them.

    Attributes:
        reasons: Human-readable drivers of the score, shown as "you
            both like ramen". Never expose raw weights to the client.
    """

    profile_id: str
    score: int = Field(ge=0, le=100)
    reasons: list[str] = []


class MatchPreview(BaseModel):
    """A ranked slice of candidates for the caller."""

    candidates: list[MatchCandidate] = []
