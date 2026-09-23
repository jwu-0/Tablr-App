# Tablr backend

Python FastAPI service. **All** business logic lives here — the Expo app has no
server code and never talks to Postgres directly.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # fill in locally; never commit
uvicorn app.main:app --reload --port 8000
```

- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Schema: http://localhost:8000/openapi.json

```bash
pytest -q          # tests
ruff check .       # lint
mypy app           # types
python scripts/export_openapi.py   # regenerate the contract
```

## Layout

```
app/
  main.py        builds the app, mounts routers, CORS
  config.py      every secret enters here (pydantic-settings)
  database.py    Postgres via the Supabase service role — server only
  deps.py        get_current_user, require_verified
  core/          security (JWT), cors (allowlist), errors
  domains/       one module per domain: schemas / router / service
```

Each domain follows the same shape:

- `schemas.py` — Pydantic models. The validated boundary; nothing untyped crosses it.
- `router.py` — endpoints. Thin: authenticate, delegate, return.
- `service.py` — the logic, including per-resource authorization.

## Swappable services

Anything buyable or risky sits behind an interface with a fake wired by
default, selected by an env flag in `config.py`:

| Domain | Interface | Default | Flag |
| --- | --- | --- | --- |
| Verification | `verification/base.py` | `fake.py` (domain allowlist + email loop) | `VERIFICATION_PROVIDER` |
| Reservations | `reservations/dispatch/base.py` | `fake.py` (logs, auto-accepts) | `RESERVATION_DISPATCH` |
| Receipts | `receipts/verify/base.py` | `fake.py` (accepts positive totals) | `RECEIPT_VERIFIER` |
| Notifications | `notifications/base.py` | `fake.py` (logs) | `NOTIFICATION_PROVIDER` |

Keep the fakes working. They are what lets the whole loop run locally with no
vendor accounts.

## Matching is the IP

`domains/matching/scoring.py` is pure functions — no database, no network, no
clock. Do not import SQLAlchemy, FastAPI, or `app.config` into it. Impure
orchestration belongs in `service.py`. Tests live beside it in
`scoring_test.py` and must stay runnable without a database.

## Data conventions (hard to change later)

- **UUID primary keys** everywhere. No sequential integers in URLs or responses.
- **TIMESTAMPTZ**, stored in UTC. Convert at display time only.
- **Money as integer minor units** (cents). Never a float, even though payments
  are deferred.
- **`public.fee_ledger` is append-only** — a trigger rejects UPDATE and DELETE.
- **Soft delete via `deleted_at`.** Every read filters it out.
- **Interest tags**: users pick canonical presets from `interest_tags`. Free
  text lands in `interest_tag_requests` and only becomes a tag once reviewed —
  this is what keeps match scores comparable.

## Security

- The backend is the **single door**. The app uses Supabase for auth only.
- The **service-role key** and `DATABASE_URL` live only here. They must never
  appear in `apps/mobile` or any committed file.
- Row-level security is enabled on every table as a second layer, default-deny.
- CORS is an explicit allowlist in `core/cors.py`. Never `*` — a wildcard origin
  with credentials is how a bearer token leaks.
- Every endpoint authenticates via `deps.py`, and the owning service decides
  whether this user may touch *this* resource.

## PII we hold

Treat this list as the answer to "what is in scope for a data request".

| Field | Where | Notes |
| --- | --- | --- |
| `.edu` email address | `profiles.email` | Identifies the student and their institution |
| Display name | `profiles.display_name` | User-chosen, shown to other students |
| Date of birth | `profiles.date_of_birth` | Stored as a date; only derived **age** is ever returned |
| Bio | `profiles.bio` | Free text; user-authored |
| Avatar image | `profiles.avatar_url` (Supabase Storage) | A face, in most cases |
| Coarse location | `profiles.home_area` (PostGIS point) | Neighbourhood-level; precise coordinates are never stored |
| Chat messages | `chat_messages.body` | Private between table members |
| Interest tags | `profile_interest_tags` | Can imply diet, religion, or community — handle as sensitive |
| Receipt images | `receipts.image_path` | May contain card fragments; never render publicly |
| Reports and appeals | `reports`, `appeals` | Accusations about identifiable people |

`GET /v1/me/export` returns all of it. `DELETE /v1/me` soft-deletes, then
purges. `consent_records` is the append-only log of what each user agreed to
and when.
