"""Group chat.

Writes go through the backend so authorization and moderation stay in
one place; delivery to other clients rides Supabase Realtime on the
`chat_messages` table.

STUB: no database access yet. Slice 7 fills these in — see
TABLR_PLAN.md.
"""

from app.core.errors import NotFoundError
from app.deps import CurrentUser
from app.domains.chat.schemas import (
    ChatMessage,
    ChatPage,
    SendMessageRequest,
)


def list_messages(
    table_id: str, user: CurrentUser, limit: int = 50
) -> ChatPage:
    """Return a page of messages. Members only."""
    # TODO(slice-7): members only, newest first, excluding deleted_at.
    _ = (table_id, user, limit)
    return ChatPage()


def send_message(
    table_id: str, user: CurrentUser, body: SendMessageRequest
) -> ChatMessage:
    """Post a message to the table's thread. Members only."""
    # TODO(slice-7): members only, run moderation on the body, then
    # insert into chat_messages.
    _ = (user, body)
    raise NotFoundError(f"No table {table_id}.")
