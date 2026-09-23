-- Reservation lifecycle. The state machine lives in the backend
-- (app/domains/reservations/service.py); this table records where it got to.
create table public.reservations (
  id                uuid primary key default gen_random_uuid(),
  table_id          uuid not null unique references public.dining_tables (id) on delete cascade,
  restaurant_id     uuid not null references public.restaurants (id),
  party_size        smallint not null,
  requested_for     timestamptz not null,
  -- pending | dispatched | confirmed | declined | cancelled | seated | no_show
  status            text not null default 'pending',
  -- Which dispatch implementation handled it: fake | email | partner_api
  dispatch_channel  text,
  dispatch_ref      text,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now()
);

create trigger reservations_set_updated_at
  before update on public.reservations
  for each row execute function public.set_updated_at();

-- Every state transition, kept for debugging and dispute resolution.
create table public.reservation_events (
  id              uuid primary key default gen_random_uuid(),
  reservation_id  uuid not null references public.reservations (id) on delete cascade,
  from_status     text,
  to_status       text not null,
  actor_id        uuid references public.profiles (id),
  detail          jsonb not null default '{}'::jsonb,
  created_at      timestamptz not null default now()
);
