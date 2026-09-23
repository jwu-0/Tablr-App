-- Per-table group chat. Delivery is Supabase Realtime for now; the backend
-- still owns writes and authorization.
create table public.chat_messages (
  id          uuid primary key default gen_random_uuid(),
  table_id    uuid not null references public.dining_tables (id) on delete cascade,
  sender_id   uuid not null references public.profiles (id) on delete cascade,
  body        text not null,
  created_at  timestamptz not null default now(),
  -- Soft delete so moderation can hide a message without breaking the thread.
  deleted_at  timestamptz
);

create index chat_messages_table_idx
  on public.chat_messages (table_id, created_at desc)
  where deleted_at is null;
