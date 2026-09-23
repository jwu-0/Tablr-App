"""Restaurant endpoints.

Browsing is open to unverified students — only acting is gated.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.deps import CurrentUserDep
from app.domains.restaurants import service
from app.domains.restaurants.schemas import (
    Restaurant,
    RestaurantPage,
    RestaurantQuery,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=RestaurantPage, summary="Browse")
async def list_restaurants(
    user: CurrentUserDep,
    query: Annotated[RestaurantQuery, Depends()],
    limit: int = Query(20, ge=1, le=100),
) -> RestaurantPage:
    """Return a page of restaurants matching the query."""
    _ = user
    return service.list_restaurants(query, limit)


@router.get("/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(
    restaurant_id: str, user: CurrentUserDep
) -> Restaurant:
    """Return one restaurant by id."""
    _ = user
    return service.get_restaurant(restaurant_id)
