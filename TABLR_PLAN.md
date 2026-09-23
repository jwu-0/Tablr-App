# Tablr Plan

The build plan: what the scaffold established, and what each vertical slice
fills in. Every file in the repo exists and runs. The slices below
replace stubs with behaviour.

`TODO(slice-N)` comments in the code point back to the sections here.

Decisions this plan deliberately leaves open — data access, dependency
injection, conventions — are in [TODO.md](TODO.md).

**Contents**

- [Ground rules](#ground-rules)
- [The repo](#the-repo)
- [What each file is](#what-each-file-is)
- [Still outstanding from the scaffold](#still-outstanding-from-the-scaffold)
- [Slices 1–9 — the core loop](#slices-19--the-core-loop)
- [After the loop closes](#after-the-loop-closes)

---

## Ground rules

Decisions that are settled. 

| Decision | Detail |
| --- | --- |
| One app | Expo (React Native) universal — iOS, Android, and web from a single codebase, with Expo Router. |
| Styling | NativeWind. Tokens live in `apps/mobile/src/lib/theme/tokens.ts`; `tailwind.config.js` reads them. |
| Backend | Python FastAPI in `backend/`. All business logic. The Expo app has no server code. |
| Buy, don't build | Supabase for Postgres + Auth + Storage + Realtime. Expo Push for notifications. Verification, email, maps, moderation, and error monitoring are external and stubbed. |
| Contract | FastAPI emits OpenAPI → a typed TS client is generated into the app. This is the only seam between the two stacks. |
| Single door | The app talks to the Python backend for all business data, and uses the Supabase client for auth only. The anon key may ship in the app; the service-role key and every other secret live only in `backend/`. |
| Repo | pnpm monorepo, frontend and backend physically separate, CODEOWNERS enforced. |

**Working style**

- Build in vertical slices. A slice touches the app *and* the backend and ends
  with something a person can do.
- Keep unbuilt pieces stubbed and runnable. The repo must always boot.
- Anything buyable or risky goes behind a `base` / `fake` / `real` triple, with
  the fake wired until told otherwise.
- The Figma export (Vite + Radix + MUI + shadcn) is **visual reference only**.
  Never install those packages into the Expo app; rebuild screens in React Native.

---

## The repo

Everything below exists and runs today. Generated files and local-only
files (`node_modules/`, `.venv/`, `apps/mobile/.env`) are omitted.

```
tablr/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── CODEOWNERS
├── apps/
│   ├── mobile/
│   │   ├── assets/
│   │   │   └── ...
│   │   ├── public/
│   │   │   └── mockServiceWorker.js
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── (auth)/
│   │   │   │   │   ├── _layout.tsx
│   │   │   │   │   ├── login.tsx
│   │   │   │   │   ├── signup.tsx
│   │   │   │   │   ├── verify.tsx
│   │   │   │   │   └── welcome.tsx
│   │   │   │   ├── (tabs)/
│   │   │   │   │   ├── _layout.tsx
│   │   │   │   │   ├── _layout.web.tsx
│   │   │   │   │   ├── add.tsx
│   │   │   │   │   ├── discover.tsx
│   │   │   │   │   ├── friends.tsx
│   │   │   │   │   ├── profile.tsx
│   │   │   │   │   └── tables.tsx
│   │   │   │   ├── _layout.tsx
│   │   │   │   └── index.tsx
│   │   │   ├── components/
│   │   │   │   ├── ui/
│   │   │   │   │   ├── avatar.tsx
│   │   │   │   │   ├── button.tsx
│   │   │   │   │   ├── card.tsx
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── input.tsx
│   │   │   │   │   └── tag.tsx
│   │   │   │   └── coming-soon.tsx
│   │   │   ├── features/
│   │   │   │   ├── chat/
│   │   │   │   │   └── queries.ts
│   │   │   │   ├── matching/
│   │   │   │   │   └── queries.ts
│   │   │   │   ├── profiles/
│   │   │   │   │   └── queries.ts
│   │   │   │   ├── reservations/
│   │   │   │   │   └── queries.ts
│   │   │   │   ├── tables/
│   │   │   │   │   └── queries.ts
│   │   │   │   └── README.md
│   │   │   ├── hooks/
│   │   │   │   ├── use-auth.tsx
│   │   │   │   ├── use-current-user.ts
│   │   │   │   └── use-theme.ts
│   │   │   ├── lib/
│   │   │   │   ├── api/
│   │   │   │   │   ├── generated/
│   │   │   │   │   │   ├── README.md
│   │   │   │   │   │   └── schema.ts
│   │   │   │   │   └── index.ts
│   │   │   │   ├── supabase/
│   │   │   │   │   └── client.ts
│   │   │   │   └── theme/
│   │   │   │       ├── fonts.ts
│   │   │   │       └── tokens.ts
│   │   │   ├── mocks/
│   │   │   │   ├── browser.native.ts
│   │   │   │   ├── browser.ts
│   │   │   │   └── handlers.ts
│   │   │   ├── providers/
│   │   │   │   └── index.tsx
│   │   │   ├── screens/
│   │   │   │   ├── add-table/
│   │   │   │   │   └── index.tsx
│   │   │   │   ├── auth/
│   │   │   │   │   ├── login.tsx
│   │   │   │   │   ├── signup.tsx
│   │   │   │   │   ├── verify.tsx
│   │   │   │   │   └── welcome.tsx
│   │   │   │   ├── discover/
│   │   │   │   │   └── index.tsx
│   │   │   │   ├── friends/
│   │   │   │   │   └── index.tsx
│   │   │   │   ├── profile/
│   │   │   │   │   └── index.tsx
│   │   │   │   └── tables/
│   │   │   │       └── index.tsx
│   │   │   └── utils/
│   │   │       ├── format-date.test.ts
│   │   │       ├── format-date.ts
│   │   │       ├── money.ts
│   │   │       └── pluralize.ts
│   │   ├── .env.example
│   │   ├── .gitignore
│   │   ├── AGENTS.md
│   │   ├── app.json
│   │   ├── babel.config.js
│   │   ├── CLAUDE.md
│   │   ├── eas.json
│   │   ├── eslint.config.js
│   │   ├── expo-env.d.ts
│   │   ├── global.css
│   │   ├── jest.config.js
│   │   ├── metro.config.js
│   │   ├── nativewind-env.d.ts
│   │   ├── package.json
│   │   ├── README.md
│   │   ├── tailwind.config.js
│   │   └── tsconfig.json
│   └── restaurant-web/
│       └── README.md
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── cors.py
│   │   │   ├── errors.py
│   │   │   └── security.py
│   │   ├── domains/
│   │   │   ├── chat/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── identity/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── matching/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── scoring.py
│   │   │   │   ├── scoring_test.py
│   │   │   │   └── service.py
│   │   │   ├── notifications/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── fake.py
│   │   │   │   ├── push.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── profiles/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── receipts/
│   │   │   │   ├── verify/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── fake.py
│   │   │   │   │   └── real.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── reservations/
│   │   │   │   ├── dispatch/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   ├── fake.py
│   │   │   │   │   └── real.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── restaurants/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── tables/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── trust_safety/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── verification/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── fake.py
│   │   │   │   ├── provider.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── deps.py
│   │   └── main.py
│   ├── scripts/
│   │   ├── activate.sh
│   │   ├── export_openapi.py
│   │   └── seed.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_cors.py
│   │   └── test_health.py
│   ├── .env.example
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── README.md
├── packages/
│   └── api-schema/
│       ├── openapi.json
│       └── README.md
├── supabase/
│   ├── migrations/
│   │   ├── 20260922000100_extensions.sql
│   │   ├── 20260922000200_conventions.sql
│   │   ├── 20260922000300_identity.sql
│   │   ├── 20260922000400_taxonomy.sql
│   │   ├── 20260922000500_restaurants.sql
│   │   ├── 20260922000600_tables.sql
│   │   ├── 20260922000700_chat.sql
│   │   ├── 20260922000800_reservations.sql
│   │   ├── 20260922000900_receipts.sql
│   │   ├── 20260922001000_trust_safety.sql
│   │   ├── 20260922001100_ledger.sql
│   │   ├── 20260922001200_consent.sql
│   │   └── 20260922001900_rls.sql
│   ├── config.toml
│   └── seed.sql
├── .env.example
├── .gitattributes
├── .gitignore
├── .npmrc
├── CLAUDE.md
├── package.json
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
├── README.md
└── TABLR_PLAN.md
```

---

## What each file is

The scaffold, laid down across phases 0–7. Grouped to match the tree.

### Root

- `package.json` — workspace scripts. `dev:mobile`, `dev:backend`, `codegen`, `lint`, `format`, `typecheck`, `test`. Everything is driven from here.
- `pnpm-workspace.yaml` — declares `apps/*` and `packages/*`. Sets `nodeLinker: hoisted`, because Metro cannot resolve pnpm's symlinked store, and `allowBuilds` for the few packages permitted to run install scripts.
- `.npmrc` — the same hoisting instruction for tools that read npm config rather than the workspace file.
- `.gitignore` — `.env*` except `.env.example`, plus `node_modules/`, `.expo/`, `dist/`, `__pycache__/`, `.venv/`, and the Python tool caches.
- `.gitattributes` — marks the generated client and `openapi.json` as generated so they collapse in diffs.
- `.env.example` — documents the shared env surface. Loads nothing; each stack reads its own file.
- `README.md` — getting started, Expo Go preview, the contract workflow, and the security model.
- `CLAUDE.md` — project memory for agents. Short on purpose; the conventions that differ from defaults.
- `TABLR_PLAN.md` — this file.

### `.github/`

- `workflows/ci.yml` — three jobs: the app (lint, typecheck, test), the backend (lint, format, typecheck, test), and a contract job that regenerates `openapi.json` plus the client and fails if either is stale.
- `CODEOWNERS` — the frontend/backend split. The backend owner also owns the schema, CI, CORS, auth dependencies, the generated client, and every `.env.example`.

### `apps/mobile/` — the Expo app

**Config**

- `app.json` — Expo config: name, `tablr` scheme, icons, splash, plugins, typed routes.
- `eas.json` — build profiles. `development` (dev client), `preview` (staging), `production`.
- `package.json` — app dependencies and scripts, including `codegen`.
- `tsconfig.json` — strict TypeScript, `@/*` path alias, jest types.
- `metro.config.js` — points Metro at the hoisted workspace root and wraps the config with NativeWind.
- `babel.config.js` — `jsxImportSource: 'nativewind'` plus `nativewind/babel`. Both are required for `className` to work.
- `tailwind.config.js` — reads `tokens.ts`, emits both palettes as CSS variables, and maps every semantic colour onto them. This is what stops classes and JS values drifting apart.
- `global.css` — Tailwind entry point consumed by NativeWind's Metro transformer.
- `nativewind-env.d.ts` — teaches TypeScript that RN components accept `className`.
- `expo-env.d.ts` — Expo's generated ambient types.
- `eslint.config.js` — Expo's flat config, with the generated client excluded.
- `jest.config.js` — `jest-expo` preset; tests live beside the code as `*.test.ts(x)`.
- `.env.example` — `EXPO_PUBLIC_*` only, with a warning that everything here ships in the bundle.
- `AGENTS.md` / `CLAUDE.md` — Expo-specific agent guidance (`CLAUDE.md` just includes `AGENTS.md`).
- `README.md` — the create-expo-app starter readme. Superseded by the root README; kept for the Expo-specific links.
- `.gitignore` — app-local ignores only (`.expo/`, `dist/`, `web-build/`). Everything else lives in the root file.
- `public/mockServiceWorker.js` — MSW's service worker for the web build. Regenerate with `npx msw init public/`.
- `assets/` — icons, splash art, and tab glyphs.

**`src/app/` — routes (thin by design)**

- `_layout.tsx` — root layout. Starts MSW in mock mode, mounts the providers, and holds the `Stack.Protected` auth gate that keeps signed-out users out of `(tabs)` and signed-in users out of `(auth)`.
- `index.tsx` — entry point; redirects to `/discover` or `/welcome`.
- `(auth)/_layout.tsx` — stack for the signed-out flow.
- `(auth)/welcome.tsx`, `login.tsx`, `signup.tsx`, `verify.tsx` — one-line re-exports of the matching screen.
- `(tabs)/_layout.tsx` — native bottom tab bar via `NativeTabs`: Discover, My Tables, Add, Friends, Profile.
- `(tabs)/_layout.web.tsx` — the web shell. A persistent left side-nav built on headless `expo-router/ui` instead of a tab bar.
- `(tabs)/discover.tsx`, `tables.tsx`, `add.tsx`, `friends.tsx`, `profile.tsx` — one-line re-exports.

**`src/screens/` — screen implementations**

- `discover/index.tsx` — ranked restaurants and open tables. Slices 4 and 5.
- `tables/index.tsx` — tables hosted or joined. Slice 6.
- `add-table/index.tsx` — create a table. Slice 6.
- `friends/index.tsx` — people met at past tables. After the loop closes.
- `profile/index.tsx` — own profile and settings. Slice 2.
- `auth/welcome.tsx` — the only screen with real UI so far: wordmark, tagline, two buttons.
- `auth/login.tsx`, `signup.tsx`, `verify.tsx` — placeholders. Slices 1 and 3.

**`src/components/`**

- `ui/button.tsx` — the one pressable. Variant and size maps; extend those rather than styling at call sites.
- `ui/card.tsx` — the standard raised surface.
- `ui/input.tsx` — text field with optional label and error.
- `ui/tag.tsx` — interest chip. Distinguishes canonical preset tags from user-requested ones.
- `ui/avatar.tsx` — profile image with an initials fallback.
- `ui/index.ts` — the barrel. Import from here; anything not exported is an implementation detail.
- `coming-soon.tsx` — placeholder body for unbuilt screens. Delete usages as slices land.

**`src/lib/`**

- `api/index.ts` — the typed client. Sets the base URL from `EXPO_PUBLIC_API_MODE`, attaches the Supabase JWT via middleware, and exports the shared error envelope.
- `api/generated/schema.ts` — generated from `openapi.json`. Never hand-edited.
- `api/generated/README.md` — says so, and says what to do instead.
- `supabase/client.ts` — the Supabase client, **auth only**. Anon key, with session persistence appropriate to native vs web.
- `theme/tokens.ts` — the single source of truth for colour, radius, and spacing. Light and dark palettes in shadcn token names, rebranded to Tablr.
- `theme/fonts.ts` — loads Bebas Neue, DM Sans, and Playfair Display from `@expo-google-fonts`. Family names here must match `tailwind.config.js`.

**`src/` — the rest**

- `providers/index.tsx` — every app-wide provider in one place: gesture handler, safe area, react-query, navigation theme, auth.
- `hooks/use-auth.tsx` — auth session context. The shape is stable; the body is a stub until slice 1.
- `hooks/use-current-user.ts` — the caller's Tablr profile, as distinct from their auth record. Slice 2.
- `hooks/use-theme.ts` — resolves the colour scheme to the token set.
- `features/README.md` — the rule for what belongs client-side versus in a backend service.
- `features/{matching,tables,chat,reservations,profiles}/queries.ts` — react-query hooks per domain. Empty stubs.
- `mocks/handlers.ts` — MSW handlers matching the contract. Mostly empty collections for now.
- `mocks/browser.ts` / `browser.native.ts` — start MSW. Split by platform so the web bundle never pulls in `msw/native` or vice versa.
- `utils/format-date.ts` — UTC to local display formatting. Takes `now` as an argument so it is testable.
- `utils/format-date.test.ts` — its tests.
- `utils/money.ts` — the single place integer cents become a decimal.
- `utils/pluralize.ts` — "1 seat" / "3 seats", without an i18n library yet.

### `apps/restaurant-web/`

- `README.md` — placeholder for the partner portal, with the reasoning for keeping it a separate app.

### `backend/` — the FastAPI service

**Config and packaging**

- `pyproject.toml` — dependencies, plus ruff configured to PEP 8 (79 columns for code, 72 for prose), mypy strict, and pytest.
- `Dockerfile` — dependency layer first, runs as a non-root user, no secrets baked in.
- `.env.example` — every secret name the backend reads, with no values.
- `README.md` — how to run it, the domain shape, the swap table, data conventions, and the PII inventory.

**`app/`**

- `main.py` — builds the app, mounts every domain router under `/v1`, wires CORS and error handling, exposes `/health`.
- `config.py` — the only place secrets enter the process. Also selects fake versus real for each swappable service.
- `database.py` — the engine and session factory, using the service role. Lazy; nothing queries yet.
- `deps.py` — `get_current_user` (verifies the Supabase JWT) and `require_verified` (gates joining, chatting, reserving). Browsing stays open.
- `core/security.py` — JWT verification. Falls back to unverified decoding outside production so the stack runs with no Supabase project; production refuses.
- `core/cors.py` — the explicit origin allowlist. Raises if anyone configures `*`.
- `core/errors.py` — the `TablrError` hierarchy and the handler that renders the `{"error": {"code", "message"}}` envelope.
- `app/__init__.py`, `core/__init__.py`, `domains/**/__init__.py`, `tests/__init__.py` — package markers, intentionally empty.

**`app/domains/` — one module per domain**

Each has `schemas.py` (the validated Pydantic boundary), `router.py` (thin: authenticate, delegate, return), and `service.py` (logic plus per-resource authorization).

- `identity/` — the account behind a Supabase auth user. Owns `GET /me`, and the two privacy endpoints `GET /me/export` and `DELETE /me` that exist from day one.
- `verification/` — the student gate. `base.py` is the interface, `fake.py` an allowlist plus email loop, `provider.py` the unwired vendor.
- `profiles/` — profile fields and the interest taxonomy. Age is derived; the birth date never leaves the server.
- `matching/` — `scoring.py` is pure functions with no DB, network, or clock, and is the IP. `scoring_test.py` sits beside it and runs without a database. `service.py` holds every impure concern.
- `restaurants/` — read-only catalogue for the beta, with a PostGIS distance filter to come.
- `tables/` — the group-meal lifecycle: create, open, join requests, full, reserved.
- `chat/` — per-table messages. Writes go through the backend; delivery rides Supabase Realtime.
- `reservations/` — the state machine. `TRANSITIONS` in `service.py` is the whole contract. `dispatch/{base,fake,real}.py` is the swap seam.
- `receipts/` — closes the loop. `verify/{base,fake,real}.py` is the swap seam.
- `trust_safety/` — reports, blocks, strikes, suspensions, appeals. Reachable by unverified users too.
- `notifications/` — `base.py`, `fake.py` (logs), `push.py` (Expo Push, unwired), plus device registration.

**`scripts/` and `tests/`**

- `scripts/export_openapi.py` — writes `packages/api-schema/openapi.json` with stable key ordering, so diffs show real contract changes.
- `scripts/seed.py` — test users and restaurants. Prints its plan; slice 1 makes it real.
- `scripts/activate.sh` — sourced by the root pnpm scripts to pick up `.venv` locally, and a no-op in CI.
- `tests/test_health.py` — the app boots, the schema generates, and a protected endpoint returns 401 without a token.
- `tests/test_cors.py` — localhost is added outside production, not inside it, and `*` is rejected.

### `packages/api-schema/`

- `openapi.json` — the contract. Generated by the backend; 27 paths today.
- `README.md` — the codegen workflow and how to read a diff here as an API change.

### `supabase/`

- `config.toml` — local stack config: API, Postgres 17, Studio, Inbucket for catching mail, Storage, and auth redirect URLs.
- `seed.sql` — the canonical starter tag list. Richer seeding goes through the API in `scripts/seed.py`.
- `migrations/…_extensions.sql` — pgcrypto, PostGIS, citext. PostGIS is enabled up front because adding geography columns later means a rewrite.
- `migrations/…_conventions.sql` — the `set_updated_at` and `reject_mutation` triggers, and the conventions comment every later migration follows.
- `migrations/…_identity.sql` — `profiles`, 1:1 with `auth.users`, including the coarse `home_area` point.
- `migrations/…_taxonomy.sql` — `interest_tags`, `profile_interest_tags`, and `interest_tag_requests` for free text.
- `migrations/…_restaurants.sql` — the catalogue, with a GiST index on location.
- `migrations/…_tables.sql` — `dining_tables` (named to avoid colliding with SQL tooling), `table_members`, `table_join_requests`.
- `migrations/…_chat.sql` — `chat_messages`, soft-deletable so moderation does not break threads.
- `migrations/…_reservations.sql` — `reservations` plus a `reservation_events` audit trail.
- `migrations/…_receipts.sql` — receipt submissions, totals in integer cents.
- `migrations/…_trust_safety.sql` — reports, blocks, strikes, suspensions, appeals.
- `migrations/…_ledger.sql` — the append-only `fee_ledger`. Nothing writes to it yet; it exists now because retrofitting an immutable money log onto live data is painful.
- `migrations/…_consent.sql` — append-only `consent_records`. Withdrawal is a new row, never an update.
- `migrations/…_rls.sql` — enables row-level security on every table, default-deny, with the two narrow policies the app actually needs.

---

## Slices 1–9 — the core loop

Build in this order. Each slice ends with something demonstrable.

### Slice 1 — accounts and auth

*Done when:* a student can sign up with a `.edu` address, log out, log back in,
and stay logged in across a cold start.

**App**
- [ ] Implement `signIn` / `signUp` / `signOut` in `hooks/use-auth.tsx` against
      `supabase.auth`; subscribe to `onAuthStateChange`.
- [ ] Start `isLoading` as `true` and flip it once the persisted session
      resolves, so the auth gate does not flash the wrong route.
- [ ] Build the real Login and Signup screens; validate the `.edu` domain client
      side as a courtesy, not as the gate.
- [ ] Hold the splash screen while fonts and the session load.

**Backend**
- [ ] `identity/service.get_me` reads `public.profiles`.
- [ ] Create the `profiles` row on first authenticated request (or via a
      Supabase auth webhook).
- [ ] `deps.get_current_user` populates `is_verified` from the database instead
      of defaulting to `False`.
- [ ] Remove the unverified-JWT fallback in `core/security.py` once local
      Supabase is the default.
- [ ] Fill in `scripts/seed.py`: create auth users via the admin API plus their
      profile rows.

### Slice 2 — profile and interest taxonomy

*Done when:* a student can complete a profile, pick interest tags, and view
someone else's public profile.

**App**
- [ ] Profile screen: display name, age, bio, avatar, tags.
- [ ] Tag picker backed by `GET /v1/tags`, with a "request a tag" path.
- [ ] Avatar upload to Supabase Storage.
- [ ] `useCurrentUser` queries `GET /v1/me` instead of reading from auth state.

**Backend**
- [ ] `profiles/service`: real reads and writes, including replacing
      `profile_interest_tags` atomically.
- [ ] Derive `age` from `date_of_birth`; never return the birth date.
- [ ] `request_tag` inserts into `interest_tag_requests` as `pending`.
- [ ] Decide and document the promotion path from request to canonical tag.
- [ ] Seed the canonical tag list (`supabase/seed.sql` already has a starter).

### Slice 3 — verification gate

*Done when:* an unverified student can browse Discover but cannot join, chat, or
reserve, and can verify themselves through the fake provider.

**App**
- [ ] Verify screen driving `POST /v1/verification/start` and `/confirm`.
- [ ] A persistent, dismissible banner for unverified users.
- [ ] Handle the `not_verified` error code by routing to `/verify` rather than
      showing a raw error.

**Backend**
- [ ] On `VERIFIED`, set `profiles.is_verified` and `verified_at`.
- [ ] `verification/status` reads the database.
- [ ] Send the confirmation email through the (still stubbed) email provider.
- [ ] Move `FakeVerificationProvider`'s pending map out of process memory so it
      survives a restart.
- [ ] Confirm `require_verified` is attached to every acting endpoint.

### Slice 4 — restaurants, read-only

*Done when:* Discover lists real restaurants, filtered by distance.

**App**
- [ ] Discover list with restaurant cards, loading and empty states.
- [ ] Ask for location permission; degrade gracefully when refused.
- [ ] Restaurant detail screen.

**Backend**
- [ ] `restaurants/service.list_restaurants` with `ST_DWithin` against
      `restaurants.location`, ordered by distance.
- [ ] Cursor pagination.
- [ ] `get_restaurant` returning 404 for missing or soft-deleted rows.
- [ ] Seed a real catalogue for the beta city.

### Slice 5 — matching

*Done when:* Discover is ranked by match score and each card explains why.

**Backend (the IP — do this carefully)**
- [ ] Implement `score_shared_tags`, `score_shared_cuisines`,
      `score_age_proximity`, `score_distance` in `matching/scoring.py`. Keep it
      pure.
- [ ] Rare tags should count more than common ones; a missing age or distance
      should score neutral, not zero.
- [ ] Grow `scoring_test.py`: identical profiles beat disjoint ones, distance
      decays monotonically, unknowns stay neutral, scores stay symmetric.
- [ ] `matching/service.preview_matches` projects rows into `MatchInput` and
      ranks. All impurity lives here.
- [ ] Return human-readable `reasons` alongside each score.

**App**
- [ ] Match percentage on cards, using the display font.
- [ ] Filter and sort controls on Discover.

### Slice 6 — tables and groups

*Done when:* a student can create a table, others can request to join, and the
host can accept or decline until it fills.

**App**
- [ ] Add-a-Table flow: restaurant, time, seats, vibe tags.
- [ ] My Tables: hosting and joined, upcoming first.
- [ ] Table detail with members and pending requests.
- [ ] Host actions: accept, decline, cancel.
- [ ] Celebrate a created table. The Figma design uses confetti; no RN confetti
      library is installed (they need a development build), so either pick one
      or use a lighter Reanimated flourish.

**Backend**
- [ ] `tables/service`: create, list open, list mine, get, join-request,
      resolve.
- [ ] Reject a join when the table is full, the user is already a member, or
      either party has blocked the other.
- [ ] Snapshot `match_score` on the join request so the host's view is stable
      when the model changes.
- [ ] Flip to `full` when `seats_taken == seats_total`.
- [ ] Notify the host on a new request and the requester on a decision.

### Slice 7 — group chat

*Done when:* members of a table can talk, live.

**App**
- [ ] Chat screen with an inverted list and an input bar.
- [ ] Subscribe to `chat_messages` over Supabase Realtime, scoped to the table.
- [ ] Optimistic send with a failed-message retry.

**Backend**
- [ ] `chat/service`: members-only reads and writes.
- [ ] Run message bodies through the moderation provider before insert.
- [ ] Add the RLS policy that lets members read their own table's messages
      directly, since Realtime bypasses the API.
- [ ] Soft-delete for moderation, without breaking the thread.

### Slice 8 — reservation lifecycle

*Done when:* a full table produces a reservation that moves through its states.

**App**
- [ ] Host-only "finalise and reserve" action.
- [ ] Reservation status on the table detail screen.
- [ ] Cancel, with a confirmation.

**Backend**
- [ ] `reservations/service.create_reservation`: host only, table must be full,
      insert `pending`, dispatch, record a `reservation_events` row.
- [ ] Enforce `TRANSITIONS` on every status change — no router may bypass it.
- [ ] `cancel_reservation` calls `dispatcher.cancel` and records the event.
- [ ] Keep the fake dispatcher working; it is how the loop runs locally.

### Slice 9 — receipt confirmation

*Done when:* a table can be marked completed by submitting a receipt.

**App**
- [ ] Post-meal prompt to submit a receipt.
- [ ] Camera and library capture, uploading to Supabase Storage.
- [ ] Completed state on the table.

**Backend**
- [ ] `receipts/service.submit_receipt`: members only, insert, run the verifier.
- [ ] On `VERIFIED`, mark the table `completed`.
- [ ] Treat `total_cents` as integer minor units throughout.

---

## After the loop closes

Roughly in order of likely need.

### Real providers

- [ ] Student verification: implement `verification/provider.py` against a real
      vendor and flip `VERIFICATION_PROVIDER`.
- [ ] Reservation dispatch: transactional email to restaurant hosts first, then
      a partner API. Flip `RESERVATION_DISPATCH`.
- [ ] Push: implement `notifications/push.py` against Expo Push, register device
      tokens, flip `NOTIFICATION_PROVIDER`.
- [ ] Receipt verification: OCR or a human review queue. Flip `RECEIPT_VERIFIER`.

### Trust and safety

- [ ] Wire `trust_safety/service` to the database.
- [ ] Make blocking hide content in both directions, everywhere.
- [ ] Strike expiry and computed suspensions.
- [ ] An appeal review surface.
- [ ] A moderation queue for reports.

### Restaurant portal

- [ ] Scaffold `apps/restaurant-web` as a React web app in the workspace.
- [ ] Partner auth and staff roles.
- [ ] Inbound reservation management.
- [ ] Partner-managed catalogue data, replacing the read-only seed.

### Platform

- [ ] Error monitoring wired to `ERROR_MONITORING_DSN`.
- [ ] EAS build and submit pipelines; TestFlight and Play internal testing.
- [ ] Friends: the tab exists but has no backend domain yet — decide whether it
      is a view over past tables or its own graph.
- [ ] Payments and the fee ledger. The append-only table is already there; work
      out the events before writing to it.
