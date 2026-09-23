-- Trust & safety. Stubbed now so reports have somewhere to land from day one.
create table public.reports (
  id             uuid primary key default gen_random_uuid(),
  reporter_id    uuid not null references public.profiles (id) on delete cascade,
  -- profile | table | message
  subject_type   text not null,
  subject_id     uuid not null,
  reason         text not null,
  detail         text,
  -- open | reviewing | actioned | dismissed
  status         text not null default 'open',
  created_at     timestamptz not null default now(),
  resolved_at    timestamptz
);

create table public.blocks (
  blocker_id  uuid not null references public.profiles (id) on delete cascade,
  blocked_id  uuid not null references public.profiles (id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (blocker_id, blocked_id),
  constraint blocks_not_self check (blocker_id <> blocked_id)
);

create table public.strikes (
  id           uuid primary key default gen_random_uuid(),
  profile_id   uuid not null references public.profiles (id) on delete cascade,
  report_id    uuid references public.reports (id),
  reason       text not null,
  -- Strikes expire; suspensions are computed from unexpired strikes.
  expires_at   timestamptz,
  created_at   timestamptz not null default now()
);

create table public.suspensions (
  id           uuid primary key default gen_random_uuid(),
  profile_id   uuid not null references public.profiles (id) on delete cascade,
  reason       text not null,
  starts_at    timestamptz not null default now(),
  ends_at      timestamptz,
  lifted_at    timestamptz,
  created_at   timestamptz not null default now()
);

create table public.appeals (
  id             uuid primary key default gen_random_uuid(),
  suspension_id  uuid not null references public.suspensions (id) on delete cascade,
  profile_id     uuid not null references public.profiles (id) on delete cascade,
  statement      text not null,
  -- pending | upheld | overturned
  status         text not null default 'pending',
  created_at     timestamptz not null default now(),
  resolved_at    timestamptz
);
