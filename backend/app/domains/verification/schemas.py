"""Request and response bodies for the verification endpoints."""

from pydantic import BaseModel, EmailStr

from app.domains.verification.base import VerificationStatus


class StartVerificationRequest(BaseModel):
    """Begin verification for a student email address."""

    email: EmailStr


class ConfirmVerificationRequest(BaseModel):
    """Complete verification with the token from the email."""

    reference: str
    token: str


class VerificationState(BaseModel):
    """Where the caller's verification currently stands."""

    status: VerificationStatus
    reference: str | None = None
    reason: str | None = None
