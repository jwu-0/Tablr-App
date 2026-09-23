"""Matching endpoints."""

from fastapi import APIRouter, Query

from app.deps import CurrentUserDep
from app.domains.matching import service
from app.domains.matching.schemas import MatchPreview

router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("/preview", response_model=MatchPreview)
async def preview(
    user: CurrentUserDep, limit: int = Query(20, ge=1, le=100)
) -> MatchPreview:
    """Return the caller's top candidates, highest score first."""
    return service.preview_matches(user, limit)
