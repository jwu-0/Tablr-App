# @tablr/api-schema

`openapi.json` is **the contract** between the Expo app and the Python backend.
It is the only seam between the two stacks.

## It is generated — do not hand-edit

```bash
pnpm codegen   # from the repo root
```

That runs two steps:

1. `backend/scripts/export_openapi.py` writes `openapi.json` from the live
   FastAPI app.
2. `openapi-typescript` regenerates `apps/mobile/src/lib/api/generated/schema.ts`.

Run it after **any** change to a router or a Pydantic schema, and commit both
the schema and the regenerated client in the same PR. A diff in `openapi.json`
with no matching client diff means someone edited one side by hand.

## Reading a diff

Changes here are API changes. Treat a removed path, a removed field, or a
widened-to-required field as breaking, and ship the app change first.
