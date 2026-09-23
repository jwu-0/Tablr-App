"""Pydantic schemas — the validated boundary for the identity domain."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr

#: Export rows are shaped by whatever the source table holds, so they
#: stay loosely typed rather than duplicating every domain's schema.
JsonObject = dict[str, Any]


class Me(BaseModel):
    """The caller's own account record."""

    id: str
    email: EmailStr
    display_name: str | None = None
    is_verified: bool = False
    created_at: datetime | None = None


class AccountExport(BaseModel):
    """Everything Tablr holds about the caller.

    Backs `GET /v1/me/export`. The field list doubles as the checklist
    for "what is in scope for a data request" — see the PII table in
    `backend/README.md`.
    """

    generated_at: datetime
    profile: JsonObject
    tables: list[JsonObject] = []
    messages: list[JsonObject] = []
    reservations: list[JsonObject] = []
    receipts: list[JsonObject] = []
    consents: list[JsonObject] = []


class DeleteAccountResult(BaseModel):
    """Acknowledgement that deletion was accepted.

    Attributes:
        scheduled: True once the soft delete has been recorded.
        purge_after: When the hard purge runs. Null while the retention
            window is still being decided.
    """

    scheduled: bool
    purge_after: datetime | None = None
