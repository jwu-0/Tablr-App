-- A "table" is a group meal someone is hosting. Named dining_tables because
-- `tables` collides with too much SQL tooling.
create table public.dining_tables (
  id              uuid primary key default gen_random_uuid(),
  host_id         uuid not null references public.profiles (id) on delete cascade,
  restaurant_id   uuid not null references public.restaurants (id),
  -- UTC. The restaurant's local time is derived at display time.
  scheduled_for   timestamptz not null,
  seats_total     smallint not null,
  note            text,
  vibe_tag_ids    uuid[] not null default '{}',
  -- draft | open | full | reserved | completed | cancelled
  status          text not null default 'draft',
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  deleted_at      timestamptz
);

create index dining_tables_open_idx
  on public.dining_tables (scheduled_for)
  where status = 'open' and deleted_at is null;

create trigger dining_tables_set_updated_at
  before update on public.dining_tables
  for each row execute function public.set_updated_at();

create table public.table_members (
  table_id    uuid not null references public.dining_tables (id) on delete cascade,
  profile_id  uuid not null references public.profiles (id) on delete cascade,
  -- host | guest
  role        text not null default 'guest',
  joined_at   timestamptz not null default now(),
  left_at     timestamptz,
  primary key (table_id, profile_id)
);

create table public.table_join_requests (
  id           uuid primary key default gen_random_uuid(),
  table_id     uuid not null references public.dining_tables (id) on delete cascade,
  profile_id   uuid not null references public.profiles (id) on delete cascade,
  message      text,
  -- pending | accepted | declined | withdrawn
  status       text not null default 'pending',
  -- Snapshot of the match score at request time, so the host sees what the
  -- ranking said even after the scoring model changes.
  match_score  smallint,
  created_at   timestamptz not null default now(),
  resolved_at  timestamptz,
  unique (table_id, profile_id)
);
