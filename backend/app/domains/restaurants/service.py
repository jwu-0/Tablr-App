"""Read-only restaurant catalogue for the beta.

STUB: no database access yet. Slice 4 fills these in, using the PostGIS
`location` column for the "near you" filter — see TABLR_PLAN.md.
"""

from app.core.errors import NotFoundError
from app.domains.restaurants.schemas import (
    Restaurant,
    RestaurantPage,
    RestaurantQuery,
)


def list_restaurants(
    query: RestaurantQuery, limit: int = 20
) -> RestaurantPage:
    """Return a page of restaurants matching `query`."""
    # TODO(slice-4): ST_DWithin against restaurants.location, ordered by
    # distance, with cursor pagination.
    _ = (query, limit)
    return RestaurantPage()


def get_restaurant(restaurant_id: str) -> Restaurant:
    """Return one restaurant.

    Raises:
        NotFoundError: if it is missing or soft-deleted.
    """
    # TODO(slice-4): select one where deleted_at is null.
    raise NotFoundError(f"No restaurant {restaurant_id}.")
