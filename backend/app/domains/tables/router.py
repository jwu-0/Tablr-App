"""Table endpoints.

Browsing uses `CurrentUserDep`; anything that changes state uses
`VerifiedUserDep`, so unverified students can look but not act.
"""

from fastapi import APIRouter, Query

from app.deps import CurrentUserDep, VerifiedUserDep
from app.domains.tables import service
from app.domains.tables.schemas import (
    CreateJoinRequest,
    CreateTableRequest,
    DiningTable,
    JoinRequest,
    ResolveJoinRequest,
    TablePage,
)

router = APIRouter(tags=["tables"])


@router.get("/tables", response_model=TablePage, summary="Open tables")
async def list_open_tables(
    user: CurrentUserDep, limit: int = Query(20, ge=1, le=100)
) -> TablePage:
    """Return open tables the caller could ask to join."""
    return service.list_open_tables(user, limit)


@router.get("/me/tables", response_model=TablePage, summary="My tables")
async def list_my_tables(user: CurrentUserDep) -> TablePage:
    """Return tables the caller hosts or belongs to."""
    return service.list_my_tables(user)


@router.get("/tables/{table_id}", response_model=DiningTable)
async def get_table(table_id: str, user: CurrentUserDep) -> DiningTable:
    """Return one table the caller is allowed to see."""
    return service.get_table(table_id, user)


@router.post("/tables", response_model=DiningTable, status_code=201)
async def create_table(
    body: CreateTableRequest, user: VerifiedUserDep
) -> DiningTable:
    """Host a new table."""
    return service.create_table(user, body)


@router.post(
    "/tables/{table_id}/join-requests",
    response_model=JoinRequest,
    status_code=201,
)
async def request_to_join(
    table_id: str, body: CreateJoinRequest, user: VerifiedUserDep
) -> JoinRequest:
    """Ask the host for a seat at this table."""
    return service.request_to_join(table_id, user, body)


@router.patch("/join-requests/{request_id}", response_model=JoinRequest)
async def resolve_join_request(
    request_id: str, body: ResolveJoinRequest, user: VerifiedUserDep
) -> JoinRequest:
    """Accept or decline a pending request. Host only."""
    return service.resolve_join_request(request_id, user, body.accept)
