"""Table lifecycle: create -> open -> join requests -> full -> reserved.

Authorization for *this* table (am I the host? am I a member?) belongs
here, not in the router.

STUB: no database access yet. Slice 6 fills these in — see
TABLR_PLAN.md.
"""

from app.core.errors import NotFoundError
from app.deps import CurrentUser
from app.domains.tables.schemas import (
    CreateJoinRequest,
    CreateTableRequest,
    DiningTable,
    JoinRequest,
    TablePage,
)


def list_my_tables(user: CurrentUser) -> TablePage:
    """Return tables the caller hosts or belongs to, soonest first."""
    # TODO(slice-6): union of hosted and joined, upcoming first.
    _ = user
    return TablePage()


def list_open_tables(user: CurrentUser, limit: int = 20) -> TablePage:
    """Return open tables the caller could ask to join."""
    # TODO(slice-6): status = 'open', ranked by matching.score_pair.
    _ = (user, limit)
    return TablePage()


def get_table(table_id: str, user: CurrentUser) -> DiningTable:
    """Return one table.

    Raises:
        NotFoundError: if it does not exist, or is not visible to this
            caller. Not-visible is reported as 404 rather than 403 so
            the endpoint does not confirm that a private table exists.
    """
    _ = user
    raise NotFoundError(f"No table {table_id}.")


def create_table(user: CurrentUser, body: CreateTableRequest) -> DiningTable:
    """Host a new table and take the first seat."""
    # TODO(slice-6): insert dining_tables plus a host row in
    # table_members, opening at status 'open'.
    _ = body
    raise NotFoundError("Table creation is not implemented yet.")


def request_to_join(
    table_id: str, user: CurrentUser, body: CreateJoinRequest
) -> JoinRequest:
    """Ask the host for a seat.

    Rejects when the table is full, the caller is already a member, or
    either party has blocked the other.
    """
    # TODO(slice-6): the three rejection cases above, then snapshot the
    # match score onto the request.
    _ = (user, body)
    raise NotFoundError(f"No table {table_id}.")


def resolve_join_request(
    request_id: str, user: CurrentUser, accept: bool
) -> JoinRequest:
    """Accept or decline a pending request. Host only."""
    # TODO(slice-6): on accept, insert table_members and flip the table
    # to 'full' when seats_taken == seats_total.
    _ = (user, accept)
    raise NotFoundError(f"No join request {request_id}.")
