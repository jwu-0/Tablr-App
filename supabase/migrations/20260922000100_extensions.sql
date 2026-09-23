-- Extensions. PostGIS is enabled up front because adding geography columns
-- later means rewriting the restaurants table.
create extension if not exists "pgcrypto"  with schema extensions;  -- gen_random_uuid()
create extension if not exists "postgis"   with schema extensions;  -- "near you" queries
create extension if not exists "citext"    with schema extensions;  -- case-insensitive email
