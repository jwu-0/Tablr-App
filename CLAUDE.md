# Tablr

Social dining app matching verified college students for group meals.

## Structure

- `apps/mobile` — Expo universal app (iOS/Android/web). The frontend area.
- `apps/restaurant-web` — placeholder for the partner portal. Empty for now.
- `backend` — Python FastAPI. All business logic. Do not put logic in the app.
- `packages/api-schema/openapi.json` — the contract. Regenerate the client after
  any backend change.
- `supabase` — Postgres/Auth/Storage config + migrations (schema source of truth).

## Commands

Run from the repo root. pnpm is the package manager (`corepack enable pnpm`).

- `pnpm dev:mobile` / `pnpm dev:backend`
- `pnpm codegen` — backend OpenAPI → `openapi.json` → typed TS client
- `pnpm lint` / `pnpm typecheck` / `pnpm test`

The backend needs its venv active: `cd backend && source .venv/bin/activate`.

In `apps/mobile`, install packages with `npx expo install <pkg>`, never a bare
`pnpm add` — it resolves the SDK-compatible version.

## Conventions (these differ from defaults — follow them)

- The backend is **Python**. Never add server logic to the Expo app.
- The app uses the Supabase client for **auth only**; all data goes through the
  Python API via `@/lib/api`.
- The service-role key and every other secret live only in `backend/`. The app
  holds `EXPO_PUBLIC_*` values only — they ship in the bundle and are public.
- CORS is an explicit allowlist in `backend/app/core/cors.py`. Never `"*"`.
- UUID primary keys; UTC `TIMESTAMPTZ`; money as integer cents;
  `public.fee_ledger` and `public.consent_records` are append-only.
- Soft delete via `deleted_at`. Every read filters it out.
- Interest tags come from the canonical `interest_tags` table. Free text goes to
  `interest_tag_requests` and is not a tag until reviewed.
- Do not edit `apps/mobile/src/lib/api/generated/` — it is generated.
- Buyable or risky services use a `base`/`fake`/`real` triple selected by an env
  flag. The fakes are wired; keep them working.
- Build in vertical slices; keep unbuilt pieces stubbed and runnable.

## Frontend specifics

- Routes in `apps/mobile/src/app/` stay thin — one line re-exporting a screen.
  Real UI lives in `src/screens/` and `src/components/`.
- Styling is NativeWind. Colours come from `src/lib/theme/tokens.ts`, which
  `tailwind.config.js` reads — never inline a hex.
- Tabs use `NativeTabs` on native and `expo-router/ui` in `(tabs)/_layout.web.tsx`
  for the web side-nav.
- `EXPO_PUBLIC_API_MODE=mock` runs the whole app against MSW with no backend.

## Backend specifics

- Each domain is `schemas.py` (validated boundary) / `router.py` (thin) /
  `service.py` (logic and per-resource authorization).
- `deps.py`: `get_current_user` verifies the Supabase JWT; `require_verified`
  gates joining, chatting, and reserving. Browsing stays open.
- `domains/matching/scoring.py` is pure functions — no DB, no network, no clock.
  This is the IP. Keep it that way and keep `scoring_test.py` runnable without a
  database.

## Where things are unfinished

Everything is scaffolded and stubbed. [TABLR_PLAN.md](TABLR_PLAN.md) has the
phase and slice breakdown; `TODO(slice-N)` comments in the code point back to it.
