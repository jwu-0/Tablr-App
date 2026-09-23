-- Receipt confirmation closes the loop: proof the group actually ate.
create table public.receipts (
  id              uuid primary key default gen_random_uuid(),
  table_id        uuid not null references public.dining_tables (id) on delete cascade,
  submitted_by    uuid not null references public.profiles (id),
  image_path      text,
  -- Integer minor units (cents). Never float.
  total_cents     integer,
  currency        char(3) not null default 'USD',
  -- pending | verified | rejected
  status          text not null default 'pending',
  -- Which verify implementation ruled on it: fake | ocr | manual
  verify_channel  text,
  created_at      timestamptz not null default now(),
  verified_at     timestamptz
);
