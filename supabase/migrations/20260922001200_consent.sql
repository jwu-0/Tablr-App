-- Consent capture: what a user agreed to, which version, and when.
-- Append-only — a consent record is evidence and must not be edited.
-- Withdrawal is a new row with `withdrawn = true`, not an update.
create table public.consent_records (
  id            uuid primary key default gen_random_uuid(),
  profile_id    uuid not null references public.profiles (id) on delete cascade,
  -- terms | privacy | location | marketing_email | push_notifications
  consent_type  text not null,
  -- Version of the document or policy the user saw.
  document_version text not null,
  withdrawn     boolean not null default false,
  -- Where consent was captured, e.g. 'signup', 'settings.location'.
  captured_at_surface text,
  created_at    timestamptz not null default now()
);

create index consent_records_latest_idx
  on public.consent_records (profile_id, consent_type, created_at desc);

create trigger consent_records_append_only
  before update or delete on public.consent_records
  for each row execute function public.reject_mutation();
