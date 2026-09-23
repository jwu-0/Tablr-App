"""Schemas for reports, blocks, suspensions, and appeals."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SubjectType(StrEnum):
    """What a report is about."""

    PROFILE = "profile"
    TABLE = "table"
    MESSAGE = "message"


class Report(BaseModel):
    """Something a user flagged for moderation."""

    id: str
    subject_type: SubjectType
    subject_id: str
    reason: str
    status: str = "open"
    created_at: datetime | None = None


class CreateReportRequest(BaseModel):
    """Flag a profile, table, or message."""

    subject_type: SubjectType
    subject_id: str
    reason: str = Field(min_length=3, max_length=100)
    detail: str | None = Field(default=None, max_length=1000)


class Block(BaseModel):
    """Somebody the caller has blocked."""

    blocked_id: str
    created_at: datetime | None = None


class CreateBlockRequest(BaseModel):
    """Block another student.

    Blocking hides content in both directions, so it also stops the
    blocked user seeing the blocker.
    """

    blocked_id: str


class Suspension(BaseModel):
    """A period during which an account cannot act."""

    id: str
    reason: str
    starts_at: datetime
    ends_at: datetime | None = None


class Appeal(BaseModel):
    """A challenge to a suspension."""

    id: str
    suspension_id: str
    status: str = "pending"


class CreateAppealRequest(BaseModel):
    """Challenge a suspension, with a written statement."""

    suspension_id: str
    statement: str = Field(min_length=10, max_length=2000)
