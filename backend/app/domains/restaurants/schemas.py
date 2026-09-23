"""Schemas for the read-only restaurant catalogue."""

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    """One restaurant in the catalogue.

    Attributes:
        price_level_cents: Rough per-head cost in integer minor units.
            Never a float — see the data conventions in the README.
        distance_km: Populated only when the request supplied a
            location.
    """

    id: str
    name: str
    address_line: str | None = None
    city: str | None = None
    price_level_cents: int | None = None
    cuisine_tags: list[str] = []
    photo_url: str | None = None
    distance_km: float | None = None


class RestaurantPage(BaseModel):
    """A cursor-paginated page of restaurants."""

    items: list[Restaurant] = []
    next_cursor: str | None = None


class RestaurantQuery(BaseModel):
    """Filters for browsing the catalogue.

    Latitude and longitude are optional: without them the results are
    unranked by distance rather than empty.
    """

    near_lat: float | None = Field(default=None, ge=-90, le=90)
    near_lng: float | None = Field(default=None, ge=-180, le=180)
    radius_km: float = Field(default=5, gt=0, le=50)
    cuisine: str | None = None
