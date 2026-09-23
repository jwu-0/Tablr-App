"""Group chat endpoints."""

from fastapi import APIRouter, Query

from app.deps import CurrentUserDep, VerifiedUserDep
from app.domains.chat import service
from app.domains.chat.schemas import (
    ChatMessage,
    ChatPage,
    SendMessageRequest,
)

router = APIRouter(prefix="/tables/{table_id}/messages", tags=["chat"])


@router.get("", response_model=ChatPage)
async def list_messages(
    table_id: str,
    user: CurrentUserDep,
    limit: int = Query(50, ge=1, le=200),
) -> ChatPage:
    """Return a page of messages for this table."""
    return service.list_messages(table_id, user, limit)


@router.post("", response_model=ChatMessage, status_code=201)
async def send_message(
    table_id: str, body: SendMessageRequest, user: VerifiedUserDep
) -> ChatMessage:
    """Post a message to this table's thread."""
    return service.send_message(table_id, user, body)
