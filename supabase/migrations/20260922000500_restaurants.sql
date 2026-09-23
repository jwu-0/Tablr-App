-- Read-only restaurant catalogue for the beta. Partner-managed data arrives
-- with the restaurant portal.
create table public.restaurants (
  id              uuid primary key default gen_random_uuid(),
  name            text not null,
  address_line    text,
  city            text,
  region          text,
  postal_code     text,
  location        extensions.geography(point, 4326),
  -- Rough per-head cost in cents. Integer minor units, never float.
  price_level_cents integer,
  cuisine_tags    text[] not null default '{}',
  photo_url       text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  deleted_at      timestamptz
);

create index restaurants_location_idx on public.restaurants using gist (location);

create trigger restaurants_set_updated_at
  before update on public.restaurants
  for each row execute function public.set_updated_at();
