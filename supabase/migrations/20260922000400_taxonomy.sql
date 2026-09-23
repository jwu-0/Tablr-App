-- Interest tag taxonomy.
--
-- Rule: users pick from `interest_tags` (canonical presets). Free text goes to
-- `interest_tag_requests` and never becomes a tag until an admin promotes it —
-- this keeps matching comparable and stops the tag space fragmenting.
create table public.interest_tags (
  id          uuid primary key default gen_random_uuid(),
  slug        text not null unique,
  label       text not null,
  -- cuisine | diet | vibe | community | activity
  category    text not null,
  is_preset   boolean not null default true,
  created_at  timestamptz not null default now(),
  deleted_at  timestamptz
);

create table public.profile_interest_tags (
  profile_id  uuid not null references public.profiles (id) on delete cascade,
  tag_id      uuid not null references public.interest_tags (id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (profile_id, tag_id)
);

-- Free-text tags a user asked for. Maps to a canonical tag once reviewed.
create table public.interest_tag_requests (
  id            uuid primary key default gen_random_uuid(),
  profile_id    uuid not null references public.profiles (id) on delete cascade,
  raw_text      text not null,
  -- set when an admin maps the request onto a canonical tag
  mapped_tag_id uuid references public.interest_tags (id),
  -- pending | mapped | rejected
  status        text not null default 'pending',
  created_at    timestamptz not null default now(),
  reviewed_at   timestamptz
);
