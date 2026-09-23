"""Schemas for receipt confirmation."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.domains.receipts.verify.base import ReceiptStatus


class Receipt(BaseModel):
    """A receipt submitted against a table.

    Attributes:
        total_cents: Integer minor units, never a float.
    """

    id: str
    table_id: str
    submitted_by: str
    image_path: str | None = None
    total_cents: int | None = Field(default=None, ge=0)
    currency: str = "USD"
    status: ReceiptStatus = ReceiptStatus.PENDING
    created_at: datetime | None = None


class SubmitReceiptRequest(BaseModel):
    """Submit a receipt for a table the caller belongs to.

    Attributes:
        image_path: Supabase Storage path. The client uploads the image
            directly and sends only the path, so receipt photos never
            pass through the API.
    """

    image_path: str | None = None
    total_cents: int | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
