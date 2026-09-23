-- Tablr's own user record, 1:1 with auth.users.
-- Supabase owns credentials; this row owns everything Tablr knows about a person.
create table public.profiles (
  id                uuid primary key references auth.users (id) on delete cascade,
  email             citext not null unique,
  display_name      text,
  -- PII. Stored as a date so age is derived, never a stale integer.
  date_of_birth     date,
  bio               text,
  avatar_url        text,
  -- .edu verification gate. False until the verification domain says otherwise.
  is_verified       boolean not null default false,
  verified_at       timestamptz,
  -- Coarse location for "near you"; precise coordinates are never stored.
  home_area         extensions.geography(point, 4326),
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),
  deleted_at        timestamptz
);

create index profiles_home_area_idx on public.profiles using gist (home_area);
create index profiles_active_idx on public.profiles (id) where deleted_at is null;

create trigger profiles_set_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();
