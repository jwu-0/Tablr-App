-- Row-level security: defence in depth.
--
-- The Python backend is the primary door and connects with the service role,
-- which bypasses RLS. These policies exist so that a leaked anon key, or a
-- future direct-from-client query, cannot read the whole database.
--
-- Default-deny: enabling RLS with no policy blocks everything. Policies are
-- added per table below, and only for the narrow cases the app genuinely needs
-- (which today is almost nothing, because the app only uses Supabase for auth).

alter table public.profiles              enable row level security;
alter table public.interest_tags         enable row level security;
alter table public.profile_interest_tags enable row level security;
alter table public.interest_tag_requests enable row level security;
alter table public.restaurants           enable row level security;
alter table public.dining_tables         enable row level security;
alter table public.table_members         enable row level security;
alter table public.table_join_requests   enable row level security;
alter table public.chat_messages         enable row level security;
alter table public.reservations          enable row level security;
alter table public.reservation_events    enable row level security;
alter table public.receipts              enable row level security;
alter table public.reports               enable row level security;
alter table public.blocks                enable row level security;
alter table public.strikes               enable row level security;
alter table public.suspensions           enable row level security;
alter table public.appeals               enable row level security;
alter table public.fee_ledger            enable row level security;
alter table public.consent_records       enable row level security;

-- Force RLS for table owners too, so a misconfigured role cannot slip past.
alter table public.fee_ledger      force row level security;
alter table public.consent_records force row level security;

-- ---------------------------------------------------------------------------
-- The only policies granted to authenticated clients today.
-- Everything else stays default-deny; add a policy here only when the app has
-- a concrete need that cannot go through the backend.
-- ---------------------------------------------------------------------------

-- A user may read their own profile row.
create policy profiles_select_own
  on public.profiles for select
  to authenticated
  using (id = (select auth.uid()) and deleted_at is null);

-- The canonical tag list is public reference data.
create policy interest_tags_select_all
  on public.interest_tags for select
  to authenticated
  using (deleted_at is null);
