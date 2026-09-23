-- Project-wide conventions, applied by every later migration.
--
--   * UUID primary keys — never expose a sequential integer in a URL or payload.
--   * TIMESTAMPTZ, stored in UTC; convert at display time only.
--   * Money as integer minor units (cents) — never float, never numeric-as-money.
--   * Soft delete via `deleted_at`; queries must filter it out.
--   * RLS on every table, default-deny (see 20260922001900_rls.sql).

-- Keeps `updated_at` honest without the application having to remember.
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- Blocks UPDATE/DELETE on append-only tables (the fee ledger, consent records).
create or replace function public.reject_mutation()
returns trigger
language plpgsql
as $$
begin
  raise exception 'table %.% is append-only', tg_table_schema, tg_table_name;
end;
$$;
