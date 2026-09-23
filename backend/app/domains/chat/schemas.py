"""Schemas for per-table group chat."""

from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """One message in a table's thread."""

    id: str
    table_id: str
    sender_id: str
    body: str
    created_at: datetime


class SendMessageRequest(BaseModel):
    """Post a message to a table the caller belongs to."""

    body: str = Field(min_length=1, max_length=2000)


class ChatPage(BaseModel):
    """A cursor-paginated page of messages, newest first."""

    items: list[ChatMessage] = []
    next_cursor: str | None = None
