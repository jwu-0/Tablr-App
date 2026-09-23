-- Append-only fee ledger.
--
-- Payments are deferred, but the ledger is created now because retrofitting an
-- immutable money log onto live data is painful. Nothing writes to it yet.
--
-- Rules: insert only, integer minor units, no updates, no deletes.
create table public.fee_ledger (
  id             uuid primary key default gen_random_uuid(),
  -- reservation_fee | no_show_fee | refund | adjustment
  event_type     text not null,
  profile_id     uuid references public.profiles (id),
  table_id       uuid references public.dining_tables (id),
  -- Signed integer minor units. Credits negative, debits positive.
  amount_cents   integer not null,
  currency       char(3) not null default 'USD',
  -- Idempotency key from whichever upstream system produced the event.
  external_ref   text unique,
  detail         jsonb not null default '{}'::jsonb,
  created_at     timestamptz not null default now()
);

create trigger fee_ledger_append_only
  before update or delete on public.fee_ledger
  for each row execute function public.reject_mutation();
