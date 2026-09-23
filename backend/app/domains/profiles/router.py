"""Profile and interest-tag endpoints."""

from fastapi import APIRouter

from app.deps import CurrentUserDep
from app.domains.profiles import service
from app.domains.profiles.schemas import (
    CreateTagRequest,
    InterestTag,
    PublicProfile,
    TagRequest,
    UpdateProfileRequest,
)

router = APIRouter(tags=["profiles"])


@router.get("/profiles/{profile_id}", response_model=PublicProfile)
async def read_profile(profile_id: str, user: CurrentUserDep) -> PublicProfile:
    """Return another student's public profile."""
    # TODO(slice-2): 404 if blocked in either direction.
    _ = user
    return service.get_profile(profile_id)


@router.patch("/me/profile", response_model=PublicProfile)
async def update_my_profile(
    body: UpdateProfileRequest, user: CurrentUserDep
) -> PublicProfile:
    """Apply a partial update to the caller's own profile."""
    return service.update_my_profile(user, body)


@router.get(
    "/tags", response_model=list[InterestTag], summary="Canonical tags"
)
async def list_tags() -> list[InterestTag]:
    """Return the canonical tag list users pick from."""
    return service.list_tags()


@router.post("/tags/requests", response_model=TagRequest, status_code=201)
async def request_tag(
    body: CreateTagRequest, user: CurrentUserDep
) -> TagRequest:
    """Ask for a tag that does not exist yet."""
    return service.request_tag(user, body)
