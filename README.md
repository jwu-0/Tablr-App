# Tablr

Tablr is a cross-platform iOS/Android social dining app with a corresponding web app.
It matches verified college students with similar interests for group meals at local restaurants.

> **Status: scaffold.** Every file below exists, compiles, and runs — but returns stub
> data. Features will get filled in as vertical slices — see [TABLR_PLAN.md](TABLR_PLAN.md).
> (This plan is tentative and will need updating over time!) Decisions currently left open
> are in [TODO.md](TODO.md) which isn't committed as it is a temporary file. 

## Layout

| Path | What it is | Owner |
| --- | --- | --- |
| `apps/mobile` | Expo universal app — iOS, Android, web from one codebase | frontend |
| `apps/restaurant-web` | Placeholder for the restaurant partner portal | frontend |
| `backend` | Python FastAPI service — **all** business logic | backend |
| `packages/api-schema` | `openapi.json` — the only seam between the two | backend |
| `supabase` | Postgres/Auth/Storage config + migrations (schema source of truth) | backend |

## Getting started

```bash
corepack enable pnpm        # once
pnpm install

# Frontend only — runs fully against MSW mocks, no backend and no secrets needed.
cp apps/mobile/.env.example apps/mobile/.env
pnpm dev:mobile

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in real values locally
cd .. && pnpm dev:backend   # http://localhost:8000/docs
```

## Previewing the app in Expo Go

Expo Go is the quickest way to see the app on a real phone. It works today because nothing in `apps/mobile`
depends on a native module outside the set Expo Go bundles. **If you add a
library with custom native code, Expo Go stops being an option** and you need a
development build instead (see below).

1. Install **Expo Go** from the [App Store](https://apps.apple.com/app/expo-go/id982107779)
   or [Google Play](https://play.google.com/store/apps/details?id=host.exp.exponent).

2. Put your phone and your computer on the same Wi-Fi network.

3. Start the dev server from the repo root:

   ```bash
   pnpm dev:mobile
   ```

4. Scan the QR code in the terminal — **Camera app** on iOS, **Expo Go's own
   scanner** on Android. The app downloads over the network and opens.

The default `EXPO_PUBLIC_API_MODE=mock` means the app runs against MSW with no
backend and no credentials, so this works on a fresh clone.

Useful keys while the server is running:

| Key | What it does |
| --- | --- |
| `r` | Reload the app |
| `j` | Open the debugger |
| `m` | Toggle the dev menu |
| `w` | Open the app in a web browser instead |
| `?` | Show all commands |

**If the QR code doesn't connect**, your network is probably blocking the
direct connection (common on university and corporate Wi-Fi). Tunnel through
Expo's relay instead — slower, but it gets through:

```bash
pnpm dev:mobile --tunnel
```

**To point the phone at a local backend**, `localhost` won't resolve from the
device. Use your computer's LAN address in `apps/mobile/.env`:

```bash
EXPO_PUBLIC_API_MODE=local
EXPO_PUBLIC_API_URL=http://192.168.1.42:8000   # your machine's LAN IP
```

Then add that origin to `CORS_ALLOWED_ORIGINS` in `backend/.env`, and restart
both servers — Expo only reads `.env` at startup.

### When Expo Go isn't enough

Expo Go ships a fixed set of native modules. Adding a library with its own
native code means building a development client once and installing that
instead:

```bash
npx eas-cli@latest build --profile development --platform ios
```

The `development` profile is already set up in `apps/mobile/eas.json`.

## Other ways to run it

```bash
pnpm dev:mobile --web         # browser
pnpm dev:mobile --ios         # iOS simulator (needs Xcode)
pnpm dev:mobile --android     # Android emulator (needs Android Studio)
```

## The contract

The backend owns the API shape. After changing any router or schema:

```bash
pnpm codegen   # backend OpenAPI -> packages/api-schema/openapi.json -> typed TS client
```

Never hand-edit `apps/mobile/src/lib/api/generated/`.

## Checks

```bash
pnpm lint        # eslint + ruff
pnpm typecheck   # tsc + mypy
pnpm test        # jest + pytest
```

CI runs all three against both stacks, plus a job that fails if the generated
client is out of sync with the backend.

## Security model — the "single door"

The app talks to the Python backend for all business data. It uses the Supabase
client **only** for auth. The Supabase anon key is public and lives in the app;
the service-role key and every other secret live only in `backend/`.
