"""Receipt endpoints, scoped to a table."""

from fastapi import APIRouter

from app.deps import CurrentUserDep, VerifiedUserDep
from app.domains.receipts import service
from app.domains.receipts.schemas import Receipt, SubmitReceiptRequest

router = APIRouter(prefix="/tables/{table_id}/receipt", tags=["receipts"])


@router.get("", response_model=Receipt)
async def get_receipt(table_id: str, user: CurrentUserDep) -> Receipt:
    """Return this table's receipt. Members only."""
    return service.get_receipt(table_id, user)


@router.post("", response_model=Receipt, status_code=201)
async def submit_receipt(
    table_id: str, body: SubmitReceiptRequest, user: VerifiedUserDep
) -> Receipt:
    """Submit a receipt to close out this table."""
    return await service.submit_receipt(table_id, user, body)
