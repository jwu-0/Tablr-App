-- Local development seed data.
--
-- STUB: intentionally minimal. Richer seeding lives in backend/scripts/seed.py,
-- which goes through the API so it exercises the same validation real clients do.
-- Keep anything here to reference data that must exist before the app boots.

insert into public.interest_tags (slug, label, category, is_preset)
values
  ('sushi',        'Sushi',        'cuisine',  true),
  ('tacos',        'Tacos',        'cuisine',  true),
  ('ramen',        'Ramen',        'cuisine',  true),
  ('vegetarian',   'Vegetarian',   'diet',     true),
  ('halal',        'Halal',        'diet',     true),
  ('late-night',   'Late night',   'vibe',     true),
  ('study-break',  'Study break',  'vibe',     true),
  ('first-years',  'First-years',  'community', true)
on conflict (slug) do nothing;
