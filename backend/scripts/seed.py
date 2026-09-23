"""Seed local development data: test users and a few restaurants.

STUB: prints what it would create. Slice 1 fills it in, so that a new
contributor gets a usable database from one command — see
TABLR_PLAN.md.

    python scripts/seed.py
"""

TEST_USERS = [
    {"email": "ada@example.edu", "display_name": "Ada", "is_verified": True},
    {
        "email": "brooke@example.edu",
        "display_name": "Brooke",
        "is_verified": True,
    },
    {
        "email": "unverified@example.edu",
        "display_name": "Sam",
        "is_verified": False,
    },
]

TEST_RESTAURANTS = [
    {"name": "Noodle Barn", "city": "Boston", "price_level_cents": 1800},
    {"name": "Taqueria Luz", "city": "Boston", "price_level_cents": 1400},
    {"name": "Kettle & Rye", "city": "Boston", "price_level_cents": 2600},
]


def main() -> int:
    """Print the seed plan. Does not touch the database yet."""
    # TODO(slice-1): create auth users through the Supabase admin API,
    # then insert the matching public.profiles rows and the restaurant
    # catalogue.
    print("seed.py is a stub. Would create:")
    for user in TEST_USERS:
        print(
            f"  user       {user['email']:<28} verified={user['is_verified']}"
        )
    for restaurant in TEST_RESTAURANTS:
        print(
            f"  restaurant {restaurant['name']:<28} "
            f"{restaurant['price_level_cents']}c"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
