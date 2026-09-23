"""Schemas for tables — the group meals students host and join."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class TableStatus(StrEnum):
    """Lifecycle of a table, from draft through to completed."""

    DRAFT = "draft"
    OPEN = "open"
    FULL = "full"
    RESERVED = "reserved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class JoinRequestStatus(StrEnum):
    """Lifecycle of one student's request to join a table."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    WITHDRAWN = "withdrawn"


class TableMember(BaseModel):
    """Somebody with a seat at the table."""

    profile_id: str
    display_name: str | None = None
    role: str = "guest"


class DiningTable(BaseModel):
    """A group meal.

    Attributes:
        scheduled_for: Always UTC. The client converts for display.
    """

    id: str
    host_id: str
    restaurant_id: str
    scheduled_for: datetime
    seats_total: int = Field(ge=2, le=12)
    seats_taken: int = 0
    note: str | None = None
    vibe_tag_ids: list[str] = []
    status: TableStatus = TableStatus.DRAFT
    members: list[TableMember] = []


class CreateTableRequest(BaseModel):
    """Host a new table. The host takes the first seat automatically."""

    restaurant_id: str
    scheduled_for: datetime
    seats_total: int = Field(ge=2, le=12)
    note: str | None = Field(default=None, max_length=280)
    vibe_tag_ids: list[str] = []


class TablePage(BaseModel):
    """A cursor-paginated page of tables."""

    items: list[DiningTable] = []
    next_cursor: str | None = None


class JoinRequest(BaseModel):
    """A student asking for a seat.

    Attributes:
        match_score: Snapshot taken when the request was made, so the
            host's view stays stable even after the scoring model
            changes.
    """

    id: str
    table_id: str
    profile_id: str
    message: str | None = None
    status: JoinRequestStatus = JoinRequestStatus.PENDING
    match_score: int | None = Field(default=None, ge=0, le=100)


class CreateJoinRequest(BaseModel):
    """Ask the host for a seat, with an optional note."""

    message: str | None = Field(default=None, max_length=280)


class ResolveJoinRequest(BaseModel):
    """The host's decision on a pending request."""

    accept: bool
